# Secuelas/backend/api.py
from flask import Blueprint, request, session, jsonify
from sqlalchemy import text, exc, asc
from extensions import db
from models import MissionDefinitionDB
from evaluation import compare_results
from init_db import execute_sql_script

main_api_blueprint = Blueprint('main_api', __name__)

# ---------------------------------------------------------------------------
# DB helpers
# ---------------------------------------------------------------------------

def get_all_missions_from_db():
    return MissionDefinitionDB.query.filter_by(is_active=True).order_by(asc(MissionDefinitionDB.id)).all()

def get_mission_from_db(mission_id):
    if mission_id is None:
        return None
    return MissionDefinitionDB.query.get(mission_id)

def setup_mission_db(mission_id):
    """Run this mission's setup SQL. Returns (ok, error_message)."""
    if mission_id is None:
        return False, "ID de mision invalido."
    obj = get_mission_from_db(mission_id)
    if obj is None:
        return False, f"Mision ID {mission_id} no encontrada."
    if not obj.setup_sql:
        return True, "Sin setup_sql."
    try:
        execute_sql_script(db.session, obj.setup_sql)
        return True, "DB configurada."
    except Exception as e:
        db.session.rollback()
        return False, f"Error configurando DB para mision {mission_id}: {e}"

# ---------------------------------------------------------------------------
# Core: build the JSON payload the frontend expects
# ---------------------------------------------------------------------------

def build_state():
    """
    Build and return the complete game-state dict.
    Also handles session initialisation and DB setup for the current mission.
    Returns (dict, http_status_code).
    """
    all_missions = get_all_missions_from_db()
    all_ids = [m.id for m in all_missions]

    if not all_ids:
        return {"error": "No hay misiones disponibles en la base de datos."}, 500

    # Initialise session if needed
    if 'current_mission_id' not in session or session['current_mission_id'] not in all_ids:
        session['current_mission_id'] = all_ids[0]
        session['archived_findings'] = []

    current_id = session['current_mission_id']
    show_results = session.get('mission_completed_show_results', False)
    last_id = all_ids[-1]

    # Run setup SQL (only when not in "show results" mode)
    setup_error = None
    if not show_results:
        ok, msg = setup_mission_db(current_id)
        if not ok and current_id <= last_id:
            setup_error = msg

    # Determine which mission object to display
    display_id = session.get('completed_mission_id_for_display', current_id) if show_results else current_id
    mission_obj = get_mission_from_db(display_id)

    is_final = False
    if setup_error:
        mission_data = {"id": current_id, "title": "Error de Sistema",
                        "coordinator_message_subject": "Error Critico",
                        "coordinator_message_body": setup_error}
    elif not show_results and current_id > last_id:
        mission_data = {
            "id": current_id,
            "title": "Fin de la Demostracion",
            "coordinator_message_subject": "Evaluacion Concluida",
            "coordinator_message_body": "Ha completado todas las directivas asignadas. Su desempeno ha sido registrado.",
        }
        is_final = True
    elif mission_obj:
        mission_data = {
            "id": mission_obj.id,
            "title": mission_obj.title,
            "coordinator_message_subject": mission_obj.coordinator_message_subject,
            "coordinator_message_body": mission_obj.coordinator_message_body,
        }
    else:
        mission_data = {"id": -1, "title": "Error de Sistema",
                        "coordinator_message_subject": "Mision no encontrada",
                        "coordinator_message_body": ""}

    state = {
        'mission': mission_data,
        'results': session.get('query_results'),
        'columns': session.get('column_names'),
        'error': session.get('sql_error'),
        'last_query': session.get('last_query', ''),
        'archived_findings': session.get('archived_findings', []),
        'is_final_mission': is_final,
        'mission_completed_show_results': show_results,
        'flash_messages': session.pop('_flashes', []),
    }

    # Clear per-request session keys
    if not show_results:
        session.pop('query_results', None)
        session.pop('column_names', None)
        session.pop('sql_error', None)

    return state, 200

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@main_api_blueprint.route('/game_state', methods=['GET'])
def game_state():
    """Returns full game state as JSON — no redirects."""
    state, code = build_state()
    return jsonify(state), code


@main_api_blueprint.route('/submit_query', methods=['POST'])
def submit_query():
    """Execute the player's SQL, evaluate it, update session, return new state."""
    data = request.get_json() or {}
    user_sql = data.get('sql_query', '').strip()
    session['last_query'] = user_sql

    current_id = session.get('current_mission_id', 1)
    mission = get_mission_from_db(current_id)
    mission_hint = mission.hint if mission else None

    if not mission:
        return jsonify({"error": "Mision no encontrada"}), 404

    session['mission_completed_show_results'] = False
    session.pop('sql_error', None)

    try:
        # Ensure clean DB state for this mission
        ok, err = setup_mission_db(current_id)
        if not ok:
            raise Exception(err)

        user_proxy = db.session.execute(text(user_sql))
        user_cols = list(user_proxy.keys()) if user_proxy.returns_rows else []
        user_rows = [dict(r._mapping) for r in user_proxy.fetchall()] if user_proxy.returns_rows else []

        correct_proxy = db.session.execute(text(mission.correct_query_script))
        correct_cols = list(correct_proxy.keys())
        correct_rows = [dict(r._mapping) for r in correct_proxy.fetchall()]

        is_correct, eval_msg = compare_results(
            user_rows, user_cols, correct_rows, correct_cols, mission.evaluation_options
        )

        session['query_results'] = user_rows
        session['column_names'] = user_cols

        flashes = session.setdefault('_flashes', [])
        if is_correct:
            flashes.append(('success', mission.success_message or "Consulta correcta!"))
            session['mission_completed_show_results'] = True
            session['completed_mission_id_for_display'] = current_id
        else:
            flashes.append(('warning', eval_msg))
            # Hints are now served on-demand via /get_hint — not shown automatically

    except exc.SQLAlchemyError as e:
        db.session.rollback()
        orig = getattr(e, 'orig', e)
        session['sql_error'] = f"Error de sintaxis o ejecucion: {str(orig).splitlines()[0]}"
    except Exception as e:
        db.session.rollback()
        session['sql_error'] = f"Error inesperado: {str(e)}"

    state, code = build_state()
    return jsonify(state), code


@main_api_blueprint.route('/next_mission', methods=['POST'])
def next_mission():
    """Advance to the next mission and return new state."""
    current_id = session.get('current_mission_id', 1)
    all_ids = [m.id for m in get_all_missions_from_db()]

    if session.get('mission_completed_show_results'):
        try:
            idx = all_ids.index(current_id)
            session['current_mission_id'] = all_ids[idx + 1]
        except (ValueError, IndexError):
            session['current_mission_id'] = (all_ids[-1] if all_ids else 0) + 1

    session['mission_completed_show_results'] = False
    session.pop('completed_mission_id_for_display', None)
    session.pop('query_results', None)
    session.pop('column_names', None)
    session.pop('sql_error', None)
    session['last_query'] = ''
    # Reset hint counter for new mission
    new_id = session.get('current_mission_id', 1)
    hints_used = session.get('hints_used', {})
    hints_used.pop(str(new_id), None)
    session['hints_used'] = hints_used
    session.setdefault('_flashes', []).append(('info', 'Nueva directiva recibida.'))

    state, code = build_state()
    return jsonify(state), code


@main_api_blueprint.route('/reset_progress', methods=['POST'])
def reset_progress():
    """Clear all session data and return fresh state."""
    session.clear()
    session.setdefault('_flashes', []).append(('info', 'Progreso de la simulacion reiniciado.'))
    state, code = build_state()
    return jsonify(state), code


@main_api_blueprint.route('/get_hint', methods=['POST'])
def get_hint():
    """
    Return the next hint level for the current mission.
    Hints are stored as 'hint_1 | hint_2' in the mission's hint field.
    Session tracks how many hints the player has requested per mission.
    """
    current_id = session.get('current_mission_id', 1)
    mission = get_mission_from_db(current_id)

    if not mission or not mission.hint:
        return jsonify({'hint': None, 'level': 0, 'message': 'No hay pistas disponibles para esta mision.'}), 200

    # Parse two-level hints
    raw = mission.hint
    parts = [p.strip() for p in raw.split(' | ', 1)]
    hint_1 = parts[0] if len(parts) > 0 else raw
    hint_2 = parts[1] if len(parts) > 1 else raw

    # Track hint level per mission in session
    hints_used = session.get('hints_used', {})
    mission_key = str(current_id)
    level_used = hints_used.get(mission_key, 0)

    if level_used == 0:
        # First request: vague hint
        hints_used[mission_key] = 1
        session['hints_used'] = hints_used
        return jsonify({'hint': hint_1, 'level': 1, 'has_more': hint_1 != hint_2})
    elif level_used == 1:
        # Second request: specific hint
        hints_used[mission_key] = 2
        session['hints_used'] = hints_used
        return jsonify({'hint': hint_2, 'level': 2, 'has_more': False})
    else:
        # Already used both hints
        return jsonify({'hint': hint_2, 'level': 2, 'has_more': False, 'exhausted': True})


# ---------------------------------------------------------------------------
# Debug / Admin
# ---------------------------------------------------------------------------

@main_api_blueprint.route('/debug', methods=['GET'])
def debug_info():
    """Diagnostic endpoint --shows DB missions and session state."""
    info = {}
    try:
        missions = MissionDefinitionDB.query.order_by(asc(MissionDefinitionDB.id)).all()
        info['mission_count'] = len(missions)
        info['missions'] = [
            {'id': m.id, 'title': m.title, 'is_active': m.is_active,
             'setup_statements': len(m.setup_sql),
             'correct_query': m.correct_query_script[:80]}
            for m in missions
        ]
    except Exception as e:
        info['missions_error'] = str(e)

    info['session'] = {
        'current_mission_id': session.get('current_mission_id'),
        'mission_completed_show_results': session.get('mission_completed_show_results'),
        'last_query': session.get('last_query', ''),
        'hints_used': session.get('hints_used', {}),
    }

    try:
        import config as cfg
        info['config_mission_count'] = len(cfg.MISSIONS)
        info['force_reload'] = getattr(cfg, 'FORCE_RELOAD_MISSIONS', False)
    except Exception as e:
        info['config_error'] = str(e)

    return jsonify(info)


@main_api_blueprint.route('/admin/execute_sql', methods=['POST'])
def admin_execute_sql():
    data = request.get_json() or {}
    sql_script = data.get('sql_script', '')
    try:
        result_proxy = db.session.execute(text(sql_script))
        if result_proxy.returns_rows:
            columns = list(result_proxy.keys())
            results = [dict(row._mapping) for row in result_proxy.fetchall()]
            return jsonify({'results': results, 'columns': columns})
        else:
            db.session.commit()
            return jsonify({'message': 'Comando ejecutado con exito.'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
