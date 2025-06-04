# Secuelas/views.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, render_template_string, jsonify
from sqlalchemy import text, exc, asc # Importar asc para ordenar
from extensions import db
# from config import MISSIONS # Ya no se usa directamente para cargar misiones
from models import MissionDefinitionDB # Importar el modelo de la BD
from evaluation import compare_results
from init_db import execute_sql_script
import json # Para el guardado de mission_evaluation_options

main_views = Blueprint('main_views', __name__)

def get_all_missions_from_db():
    """Obtiene todas las misiones activas de la base de datos, ordenadas por ID."""
    return MissionDefinitionDB.query.filter_by(is_active=True).order_by(asc(MissionDefinitionDB.id)).all()

def get_mission_from_db(mission_id):
    """Obtiene una misión específica de la base de datos por su ID."""
    if mission_id is None:
        return None
    return MissionDefinitionDB.query.get(mission_id)


@main_views.route('/', methods=['GET'])
def landing_page():
    return render_template('landing_page.html')

def setup_current_mission_db(mission_id):
    """Configura la base de datos para el mission_id dado usando su setup_sql desde la BD."""
    if mission_id is None:
        flash("ID de misión inválido para la configuración de la base de datos.", "error")
        return False
        
    current_mission_db_obj = get_mission_from_db(mission_id) 
    if current_mission_db_obj and current_mission_db_obj.setup_sql: 
        try:
            print(f"setup_current_mission_db: Configurando DB para Misión ID: {mission_id}")
            with current_app.app_context():
                 execute_sql_script(db.session, current_mission_db_obj.setup_sql) 
            print(f"setup_current_mission_db: DB configurada para Misión ID: {mission_id}")
            return True
        except Exception as e:
            flash(f"Error crítico al configurar la base de datos para la misión: {e}", "error")
            print(f"setup_current_mission_db: Error crítico al configurar la base de datos para la misión {mission_id}: {e}")
            return False
    elif current_mission_db_obj:
        print(f"setup_current_mission_db: No hay 'setup_sql' para la Misión ID: {mission_id}. Se asume que la DB está lista.")
        return True
    else:
        flash(f"Misión ID {mission_id} no encontrada en la base de datos para configuración.", "error")
        print(f"setup_current_mission_db: Misión ID {mission_id} no encontrada en la BD.")
        return False

@main_views.route('/game', methods=['GET'])
def game_interface():
    all_missions_db_objects = get_all_missions_from_db()
    all_mission_ids = [m.id for m in all_missions_db_objects] 

    if not all_mission_ids:
        flash("No hay misiones disponibles en este momento. Contacte al administrador.", "error")
        return redirect(url_for('main_views.landing_page'))

    if 'current_mission_id' not in session or session['current_mission_id'] not in all_mission_ids:
        session['current_mission_id'] = all_mission_ids[0] 
        session['archived_findings'] = []
    
    current_mission_id = session.get('current_mission_id')
    mission_completed_show_results = session.get('mission_completed_show_results', False)
    
    num_total_missions = len(all_mission_ids)
    last_db_mission_id = all_mission_ids[-1] if all_mission_ids else 0

    if not mission_completed_show_results:
        if current_mission_id in all_mission_ids:
            if not setup_current_mission_db(current_mission_id):
                 flash("Error al preparar el entorno de la misión. Por favor, intente de nuevo o contacte al administrador.", "error")
                 return redirect(url_for('main_views.landing_page')) 
        elif current_mission_id > last_db_mission_id and last_db_mission_id > 0: 
            pass 
        else: 
            flash(f"Error: No se puede cargar la misión ID {current_mission_id}. Volviendo al inicio.", "error")
            session.clear()
            return redirect(url_for('main_views.landing_page'))

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
            "hint": None, "success_message": None, "evaluation_options": {}
        }
        is_final_mission = True
    elif mission_object_from_db:
        mission_data_for_template_dict = {
            "id": mission_object_from_db.id,
            "title": mission_object_from_db.title,
            "coordinator_message_subject": mission_object_from_db.coordinator_message_subject,
            "coordinator_message_body": mission_object_from_db.coordinator_message_body,
            "hint": mission_object_from_db.hint,
            "success_message": mission_object_from_db.success_message,
            "evaluation_options": mission_object_from_db.evaluation_options 
        }
    else: 
        flash(f"Error: Misión ID {mission_id_to_load} no encontrada o inválida.", "error")
        mission_data_for_template_dict = { 
            "id": -1, "title": "Error de Sistema",
            "coordinator_message_subject": "Fallo en el Sistema de Misiones",
            "coordinator_message_body": "Contacte al administrador. Código de error: M_LOAD_FAIL",
            "hint": None, "success_message": None, "evaluation_options": {}
        }

    query_results = session.get('query_results', None)
    column_names = session.get('column_names', None)
    sql_error = session.get('sql_error', None)
    last_query = session.get('last_query', '')

    if not mission_completed_show_results:
        session.pop('query_results', None)
        session.pop('column_names', None)
        session.pop('sql_error', None)

    return render_template('index.html',
                           mission=mission_data_for_template_dict, 
                           results=query_results,
                           columns=column_names,
                           error=sql_error,
                           last_query=last_query,
                           archived_findings=session.get('archived_findings', []),
                           is_final_mission=is_final_mission,
                           mission_completed_show_results=mission_completed_show_results,
                           num_total_missions=num_total_missions)

@main_views.route('/submit_query', methods=['POST'])
def submit_query():
    user_sql_query = request.form.get('sql_query', '').strip()
    session['last_query'] = user_sql_query

    current_mission_id = session.get('current_mission_id', 1)
    
    # Obtener el objeto de misión de la BD
    current_mission_object = get_mission_from_db(current_mission_id)

    if not current_mission_object:
        flash("Error: No se pudo determinar la misión actual desde la BD.", "error")
        return redirect(url_for('main_views.game_interface'))

    # Extraer todos los atributos necesarios ANTES de otras operaciones de BD
    mission_eval_options = current_mission_object.evaluation_options
    mission_correct_query_script = current_mission_object.correct_query_script
    mission_success_message = current_mission_object.success_message
    mission_hint = current_mission_object.hint
    # No es necesario extraer el ID, ya lo tenemos en current_mission_id

    # Verificar si el usuario ya completó todas las misiones disponibles
    all_missions_db_objects = get_all_missions_from_db() 
    all_mission_ids = [m.id for m in all_missions_db_objects]
    last_db_mission_id = all_mission_ids[-1] if all_mission_ids else 0

    if current_mission_id > last_db_mission_id and last_db_mission_id > 0 and not session.get('mission_completed_show_results'): 
        flash("Ya ha completado todas las misiones disponibles.", "info")
        return redirect(url_for('main_views.game_interface'))

    session['mission_completed_show_results'] = False 

    restricted_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'CREATE', 'ALTER', 'GRANT', 'TRUNCATE', 'EXEC', 'PRAGMA']
    allow_restricted = mission_eval_options.get("allow_restricted_keywords", False) 
    
    query_upper = user_sql_query.upper()
    if not (query_upper.startswith("SELECT") or query_upper.startswith("WITH")) and not allow_restricted:
        session['sql_error'] = "Comando no permitido. En esta fase, solo se permiten consultas SELECT o que comiencen con WITH."
        return redirect(url_for('main_views.game_interface'))
    
    if not allow_restricted:
        for keyword in restricted_keywords:
            if f" {keyword} " in f" {query_upper} " and not (query_upper.startswith("SELECT") or query_upper.startswith("WITH")):
                session['sql_error'] = f"Comando '{keyword}' detectado y no permitido en esta misión."
                return redirect(url_for('main_views.game_interface'))

    user_query_results = None
    user_column_names = []
    is_correct = False
    eval_message = ""

    try:
        # Configurar la BD para la misión actual
        if not setup_current_mission_db(current_mission_id):
            # El error ya fue flasheado por setup_current_mission_db
            return redirect(url_for('main_views.game_interface'))

        print(f"Ejecutando consulta del usuario para Misión {current_mission_id}: {user_sql_query}")
        user_result_proxy = db.session.execute(text(user_sql_query))
        
        if user_result_proxy.returns_rows:
            user_column_names = list(user_result_proxy.keys())
            user_query_results = [dict(row._mapping) for row in user_result_proxy.fetchall()]
        else: 
            db.session.commit() # Para DML (si se permitieran)
            user_query_results = [{"status": "Comando ejecutado, no se devolvieron filas."}] 
            user_column_names = ["status"]
            
        # Usar la variable local con el script de la consulta correcta
        print(f"Ejecutando consulta correcta para Misión {current_mission_id}: {mission_correct_query_script}")
        correct_result_proxy = db.session.execute(text(mission_correct_query_script))
        
        correct_column_names = list(correct_result_proxy.keys())
        correct_query_results = [dict(row._mapping) for row in correct_result_proxy.fetchall()]
        
        # Usar la variable local con las opciones de evaluación
        is_correct, eval_message = compare_results(
            user_results=user_query_results,
            user_columns=user_column_names,
            correct_results=correct_query_results,
            correct_columns=correct_column_names,
            eval_options=mission_eval_options 
        )
        
        session['query_results'] = user_query_results 
        session['column_names'] = user_column_names
        session.pop('sql_error', None) 

        if is_correct:
            # Usar la variable local con el mensaje de éxito
            flash(mission_success_message or "¡Consulta correcta!", "success") 
            session['mission_completed_show_results'] = True
            session['completed_mission_id_for_display'] = current_mission_id
            
            if current_mission_id == 3 and user_query_results and isinstance(user_query_results, list) and user_query_results:
                 finding_summary = f"Misión {current_mission_id}: Anomalía detectada en PROYECTO_QUIMERA. {len(user_query_results)} registro(s) sospechoso(s) encontrado(s)."
                 if finding_summary not in session.get('archived_findings', []):
                     session.setdefault('archived_findings', []).append(finding_summary)
                 session.modified = True
        else: 
            flash(eval_message, "warning") 
            # Usar la variable local con la pista
            if mission_hint: 
                flash(f"PISTA: {mission_hint}", "info")
                
    except exc.SQLAlchemyError as e: 
        db.session.rollback() 
        error_message = str(e.orig) if hasattr(e, 'orig') else str(e) 
        error_message_short = error_message.split('\n')[0]
        session['sql_error'] = f"Error de Sintaxis o Ejecución: {error_message_short}"
        session.pop('query_results', None) 
        session.pop('column_names', None)
        # Usar la variable local con la pista, verificando que no sea None
        if mission_hint: 
            flash(f"PISTA: {mission_hint}", "info")
    except Exception as e: 
        db.session.rollback()
        session['sql_error'] = f"Error inesperado al procesar la consulta: {str(e)}"
        session.pop('query_results', None)
        session.pop('column_names', None)
        print(f"Error inesperado en submit_query: {e}", exc_info=True) 
    finally:
        pass

    return redirect(url_for('main_views.game_interface'))

@main_views.route('/next_mission', methods=['POST'])
def next_mission():
    current_mission_id = session.get('current_mission_id', 1)
    all_missions_db_objects = get_all_missions_from_db() 
    all_mission_ids = [m.id for m in all_missions_db_objects]
    
    if session.get('mission_completed_show_results', False) and \
       session.get('completed_mission_id_for_display') == current_mission_id:
        
        try:
            current_mission_index = all_mission_ids.index(current_mission_id)
            if current_mission_index < len(all_mission_ids) - 1:
                next_mission_obj = all_missions_db_objects[current_mission_index + 1]
                session['current_mission_id'] = next_mission_obj.id
                flash("Nueva directiva recibida.", "info")
            else: 
                last_id = all_mission_ids[-1] if all_mission_ids else 0
                session['current_mission_id'] = last_id + 1 
                flash("Todas las directivas han sido completadas. Evaluación finalizada.", "success")
        except ValueError: 
            flash("Error al avanzar de misión. Reiniciando.", "error")
            session['current_mission_id'] = all_mission_ids[0] if all_mission_ids else 1

    else:
        flash("Complete la directiva actual antes de continuar.", "warning")

    session['mission_completed_show_results'] = False
    session.pop('query_results', None)
    session.pop('column_names', None)
    session.pop('sql_error', None)
    session.pop('completed_mission_id_for_display', None)
    session['last_query'] = '' 

    return redirect(url_for('main_views.game_interface'))

@main_views.route('/reset_progress')
def reset_progress():
    session.pop('current_mission_id', None) 
    session.pop('archived_findings', None) 
    session.pop('mission_completed_show_results', None)
    session.pop('query_results', None)
    session.pop('column_names', None)
    session.pop('sql_error', None)
    session.pop('last_query', None)
    session.pop('completed_mission_id_for_display', None)
    
    flash("Progreso de la simulación reiniciado.", "info")
    return redirect(url_for('main_views.landing_page'))

# --- Rutas del Panel de Administrador ---
# (El resto de las rutas de administrador permanecen igual)
@main_views.route('/admin', methods=['GET'])
def admin_panel():
    return render_template('admin_panel.html')

@main_views.route('/admin/execute_setup_sql', methods=['POST'])
def admin_execute_setup_sql():
    data = request.get_json()
    setup_sql_script_text = data.get('setup_sql', '')
    
    statements = [s.strip() for s in setup_sql_script_text.split(';') if s.strip()]
    if not statements and setup_sql_script_text.strip():
        statements = [s.strip() for s in setup_sql_script_text.splitlines() if s.strip()]
    
    if not statements:
        return jsonify({'error': 'No se proporcionaron sentencias SQL para ejecutar.'}), 400
    try:
        with current_app.app_context():
            execute_sql_script(db.session, statements)
        return jsonify({'message': f'{len(statements)} sentencia(s) de configuración ejecutada(s) con éxito.'})
    except Exception as e:
        return jsonify({'error': f'Error al ejecutar SQL de configuración: {str(e)}'}), 500

@main_views.route('/admin/execute_correct_query', methods=['POST'])
def admin_execute_correct_query():
    data = request.get_json()
    correct_query = data.get('correct_query', '')
    setup_sql_script_text = data.get('setup_sql', '')

    if not correct_query:
        return jsonify({'error': 'No se proporcionó la consulta correcta.'}), 400
    
    query_upper = correct_query.strip().upper()
    if not (query_upper.startswith("SELECT") or query_upper.startswith("WITH")):
        return jsonify({'error': 'La "Consulta Correcta" debe ser una sentencia SELECT o comenzar con WITH.'}), 400

    setup_statements = [s.strip() for s in setup_sql_script_text.split(';') if s.strip()]
    if not setup_statements and setup_sql_script_text.strip():
        setup_statements = [s.strip() for s in setup_sql_script_text.splitlines() if s.strip()]
    try:
        with current_app.app_context():
            if setup_statements:
                print(f"Admin: Ejecutando setup_sql ANTES de la consulta correcta: {len(setup_statements)} sentencias.")
                execute_sql_script(db.session, setup_statements)
            else:
                print("Admin: No hay setup_sql para ejecutar antes de la consulta correcta.")

            print(f"Admin: Ejecutando consulta correcta: {correct_query}")
            result_proxy = db.session.execute(text(correct_query))
            
            if result_proxy.returns_rows:
                columns = list(result_proxy.keys())
                results = [dict(row._mapping) for row in result_proxy.fetchall()]
                return jsonify({'results': results, 'columns': columns})
            else:
                return jsonify({'message': 'La consulta correcta se ejecutó pero no devolvió filas.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al ejecutar la consulta correcta: {str(e)}'}), 500

@main_views.route('/admin/save_mission', methods=['POST'])
def save_mission():
    try:
        mission_id = request.form.get('mission_id', type=int)
        mission_title = request.form.get('mission_title')
        mission_subject = request.form.get('mission_subject')
        mission_body = request.form.get('mission_body')
        mission_hint = request.form.get('mission_hint')
        mission_success_message = request.form.get('mission_success_message')
        
        setup_sql_script_text = request.form.get('setup_sql') 
        correct_query_script = request.form.get('correct_query')
        
        order_matters = request.form.get('order_matters') == 'true'
        column_order_matters = request.form.get('column_order_matters') == 'true'
        check_column_names = request.form.get('check_column_names') == 'true'

        if not all([mission_id is not None, mission_title, mission_subject, mission_body, mission_success_message, setup_sql_script_text, correct_query_script]):
            flash("Todos los campos principales de la misión son obligatorios (ID, Título, Asunto, Cuerpo, Mensaje Éxito, Setup SQL, Correct Query).", "error")
            return redirect(url_for('main_views.admin_panel'))

        evaluation_options_dict = {
            'order_matters': order_matters,
            'column_order_matters': column_order_matters,
            'check_column_names': check_column_names
        }

        with current_app.app_context():
            existing_mission = MissionDefinitionDB.query.get(mission_id)
            if existing_mission: 
                existing_mission.title = mission_title
                existing_mission.coordinator_message_subject = mission_subject
                existing_mission.coordinator_message_body = mission_body
                existing_mission.setup_sql_script = setup_sql_script_text 
                existing_mission.correct_query_script = correct_query_script
                existing_mission.evaluation_options_json = json.dumps(evaluation_options_dict)
                existing_mission.hint = mission_hint
                existing_mission.success_message = mission_success_message
                existing_mission.is_active = True 
                db.session.commit()
                flash(f"Misión ID {mission_id} actualizada exitosamente en la base de datos.", "success")
            else: 
                new_mission_db = MissionDefinitionDB(
                    id=mission_id,
                    title=mission_title,
                    coordinator_message_subject=mission_subject,
                    coordinator_message_body=mission_body,
                    setup_sql_script=setup_sql_script_text, 
                    correct_query_script=correct_query_script,
                    evaluation_options_json=json.dumps(evaluation_options_dict),
                    hint=mission_hint,
                    success_message=mission_success_message,
                    is_active=True
                )
                db.session.add(new_mission_db)
                db.session.commit()
                flash(f"Misión ID {mission_id} guardada exitosamente en la base de datos.", "success")
        
    except exc.IntegrityError as e: 
        db.session.rollback()
        flash(f"Error de integridad al guardar la misión (ej. ID de misión ya existe): {str(e.orig)}", "error")
        print(f"Error de integridad en save_mission: {e}", exc_info=True)
    except Exception as e:
        db.session.rollback() 
        flash(f"Error al procesar el formulario de la misión: {str(e)}", "error")
        print(f"Error en save_mission: {e}", exc_info=True)

    return redirect(url_for('main_views.admin_panel'))
