# Secuelas/backend/api.py
from flask import Blueprint, request, session, jsonify, current_app
from sqlalchemy import text, exc, asc
from extensions import db
from models import MissionDefinitionDB
from evaluation import compare_results
from init_db import execute_sql_script
import json

# Rename the blueprint to reflect it's an API
main_api_blueprint = Blueprint('main_api', __name__)

def get_all_missions_from_db():
    """Obtiene todas las misiones activas de la base de datos, ordenadas por ID."""
    return MissionDefinitionDB.query.filter_by(is_active=True).order_by(asc(MissionDefinitionDB.id)).all()

def get_mission_from_db(mission_id):
    """Obtiene una misión específica de la base de datos por su ID."""
    if mission_id is None:
        return None
    return MissionDefinitionDB.query.get(mission_id)

def setup_current_mission_db(mission_id):
    """Configura la base de datos para el mission_id dado usando su setup_sql desde la BD."""
    if mission_id is None:
        return False, "ID de misión inválido."
        
    current_mission_db_obj = get_mission_from_db(mission_id) 
    if current_mission_db_obj and current_mission_db_obj.setup_sql: 
        try:
            with current_app.app_context():
                 execute_sql_script(db.session, current_mission_db_obj.setup_sql) 
            return True, "DB configurada."
        except Exception as e:
            return False, f"Error crítico al configurar la base de datos para la misión: {e}"
    elif current_mission_db_obj:
        return True, "No hay 'setup_sql' para la Misión. Se asume que la DB está lista."
    else:
        return False, f"Misión ID {mission_id} no encontrada."

@main_api_blueprint.route('/game_state', methods=['GET'])
def game_state():
    """Returns the complete current state of the game for the frontend."""
    all_missions_db_objects = get_all_missions_from_db()
    all_mission_ids = [m.id for m in all_missions_db_objects] 

    if not all_mission_ids:
        return jsonify({"error": "No hay misiones disponibles."}), 500

    if 'current_mission_id' not in session or session['current_mission_id'] not in all_mission_ids:
        session['current_mission_id'] = all_mission_ids[0] 
        session['archived_findings'] = []
    
    current_mission_id = session.get('current_mission_id')
    mission_completed_show_results = session.get('mission_completed_show_results', False)
    
    last_db_mission_id = all_mission_ids[-1] if all_mission_ids else 0

    if not mission_completed_show_results:
        success, message = setup_current_mission_db(current_mission_id)
        if not success and current_mission_id <= last_db_mission_id:
            return jsonify({"error": message}), 500

    is_final_mission = False
    mission_data_for_template_dict = None

    mission_id_to_load = current_mission_id
    if mission_completed_show_results:
        mission_id_to_load = session.get('completed_mission_id_for_display', current_mission_id)
    
    mission_object_from_db = get_mission_from_db(mission_id_to_load)

    if not mission_completed_show_results and current_mission_id > last_db_mission_id and last_db_mission_id > 0 :
        mission_data_for_template_dict = { 
            "id": current_mission_id, 
            "title": "Fin de la Demostración",
            "coordinator_message_subject": "Evaluación Concluida",
            "coordinator_message_body": "Ha completado todas las directivas asignadas. Su desempeño ha sido registrado.",
        }
        is_final_mission = True
    elif mission_object_from_db:
        mission_data_for_template_dict = {
            "id": mission_object_from_db.id,
            "title": mission_object_from_db.title,
            "coordinator_message_subject": mission_object_from_db.coordinator_message_subject,
            "coordinator_message_body": mission_object_from_db.coordinator_message_body,
        }
    else: 
         mission_data_for_template_dict = { "id": -1, "title": "Error de Sistema" }

    state = {
        'mission': mission_data_for_template_dict,
        'results': session.get('query_results'),
        'columns': session.get('column_names'),
        'error': session.get('sql_error'),
        'last_query': session.get('last_query', ''),
        'archived_findings': session.get('archived_findings', []),
        'is_final_mission': is_final_mission,
        'mission_completed_show_results': mission_completed_show_results,
        'flash_messages': session.pop('_flashes', []) # Pop flashes to send to frontend
    }
    
    # Clear session data that should not persist between state fetches
    if not mission_completed_show_results:
        session.pop('query_results', None)
        session.pop('column_names', None)
        session.pop('sql_error', None)

    return jsonify(state)

@main_api_blueprint.route('/submit_query', methods=['POST'])
def submit_query():
    data = request.get_json()
    user_sql_query = data.get('sql_query', '').strip()
    session['last_query'] = user_sql_query
    
    current_mission_id = session.get('current_mission_id', 1)
    current_mission_object = get_mission_from_db(current_mission_id)

    if not current_mission_object:
        session['_flashes'] = [('error', "Error: No se pudo determinar la misión actual.")]
        return jsonify({"error": "Misión no encontrada"}), 404

    mission_eval_options = current_mission_object.evaluation_options
    mission_correct_query_script = current_mission_object.correct_query_script
    mission_success_message = current_mission_object.success_message
    mission_hint = current_mission_object.hint

    session['mission_completed_show_results'] = False 

    # --- Query validation and execution logic (mostly unchanged) ---
    try:
        if not setup_current_mission_db(current_mission_id)[0]:
             raise Exception("Fallo en la configuración de la BD de la misión.")
        
        user_result_proxy = db.session.execute(text(user_sql_query))
        
        user_column_names = list(user_result_proxy.keys()) if user_result_proxy.returns_rows else []
        user_query_results = [dict(row._mapping) for row in user_result_proxy.fetchall()] if user_result_proxy.returns_rows else []

        correct_result_proxy = db.session.execute(text(mission_correct_query_script))
        correct_column_names = list(correct_result_proxy.keys())
        correct_query_results = [dict(row._mapping) for row in correct_result_proxy.fetchall()]
        
        is_correct, eval_message = compare_results(user_query_results, user_column_names, correct_query_results, correct_column_names, mission_eval_options)
        
        session['query_results'] = user_query_results 
        session['column_names'] = user_column_names
        session.pop('sql_error', None) 

        flashes = session.setdefault('_flashes', [])
        if is_correct:
            flashes.append(('success', mission_success_message or "¡Consulta correcta!"))
            session['mission_completed_show_results'] = True
            session['completed_mission_id_for_display'] = current_mission_id
        else: 
            flashes.append(('warning', eval_message))
            if mission_hint: 
                flashes.append(('info', f"PISTA: {mission_hint}"))
                
    except exc.SQLAlchemyError as e: 
        db.session.rollback() 
        session['sql_error'] = f"Error de Sintaxis o Ejecución: {str(e.orig).splitlines()[0]}"
        flashes = session.setdefault('_flashes', [])
        if mission_hint: flashes.append(('info', f"PISTA: {mission_hint}"))
    except Exception as e: 
        db.session.rollback()
        session['sql_error'] = f"Error inesperado: {str(e)}"

    return redirect(url_for('main_api.game_state')) # Redirect to GET the new state

@main_api_blueprint.route('/next_mission', methods=['POST'])
def next_mission():
    current_mission_id = session.get('current_mission_id', 1)
    all_missions = get_all_missions_from_db()
    all_mission_ids = [m.id for m in all_missions]
    
    if session.get('mission_completed_show_results'):
        try:
            current_idx = all_mission_ids.index(current_mission_id)
            session['current_mission_id'] = all_mission_ids[current_idx + 1]
        except (ValueError, IndexError):
            session['current_mission_id'] = (all_mission_ids[-1] if all_mission_ids else 0) + 1
    
    session['mission_completed_show_results'] = False
    session.pop('completed_mission_id_for_display', None)
    session['last_query'] = '' 
    session.setdefault('_flashes', []).append(('info', 'Nueva directiva recibida.'))
    
    return redirect(url_for('main_api.game_state'))

@main_api_blueprint.route('/reset_progress', methods=['POST'])
def reset_progress():
    session.clear()
    session.setdefault('_flashes', []).append(('info', 'Progreso de la simulación reiniciado.'))
    return redirect(url_for('main_api.game_state'))

# Admin routes remain largely the same, just returning JSON
@main_api_blueprint.route('/admin/execute_sql', methods=['POST'])
def admin_execute_sql():
    data = request.get_json()
    sql_script = data.get('sql_script', '')
    
    try:
        # For simplicity, we execute the whole block. For multiple statements, split them.
        result_proxy = db.session.execute(text(sql_script))
        if result_proxy.returns_rows:
            columns = list(result_proxy.keys())
            results = [dict(row._mapping) for row in result_proxy.fetchall()]
            return jsonify({'results': results, 'columns': columns})
        else:
            db.session.commit()
            return jsonify({'message': 'Comando ejecutado con éxito, no se devolvieron filas.'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
