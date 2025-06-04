# Secuelas/views.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, render_template_string, jsonify
from sqlalchemy import text, exc
from extensions import db
from config import MISSIONS
from evaluation import compare_results
from init_db import execute_sql_script

main_views = Blueprint('main_views', __name__)

@main_views.route('/', methods=['GET'])
def landing_page():
    return render_template('landing_page.html')

def setup_current_mission_db(mission_id):
    current_mission = next((m for m in MISSIONS if m['id'] == mission_id), None)
    if current_mission and 'setup_sql' in current_mission:
        try:
            print(f"setup_current_mission_db: Configurando DB para Misión ID: {mission_id}")
            with current_app.app_context():
                 execute_sql_script(db.session, current_mission['setup_sql'])
            print(f"setup_current_mission_db: DB configurada para Misión ID: {mission_id}")
            return True
        except Exception as e:
            flash(f"Error crítico al configurar la base de datos para la misión: {e}", "error")
            print(f"setup_current_mission_db: Error crítico al configurar la base de datos para la misión {mission_id}: {e}")
            return False
    elif current_mission:
        print(f"setup_current_mission_db: No hay 'setup_sql' para la Misión ID: {mission_id}. Se asume que la DB está lista.")
        return True
    else:
        flash(f"Misión ID {mission_id} no encontrada para configuración de DB.", "error")
        print(f"setup_current_mission_db: Misión ID {mission_id} no encontrada.")
        return False

@main_views.route('/game', methods=['GET'])
def game_interface():
    if 'current_mission_id' not in session:
        session['current_mission_id'] = 1 
        session['archived_findings'] = []
    
    current_mission_id = session.get('current_mission_id', 1)
    mission_completed_show_results = session.get('mission_completed_show_results', False)
    
    if not mission_completed_show_results:
        # Solo configurar la BD si el ID de misión es válido y existe
        if any(m['id'] == current_mission_id for m in MISSIONS):
            if not setup_current_mission_db(current_mission_id):
                 # Si setup_current_mission_db ya flashea el error, no necesitamos hacerlo aquí.
                 # Podríamos redirigir a una página de error o a la landing page.
                 return redirect(url_for('main_views.landing_page')) # Ejemplo de redirección
        elif current_mission_id > len(MISSIONS): # Ya pasó la última misión
            pass # Se manejará abajo para mostrar "Fin de la Demostración"
        else: # ID de misión inválido o no encontrado, pero no es el fin.
            flash(f"Error: No se puede cargar la misión ID {current_mission_id}. Volviendo al inicio.", "error")
            session.clear() # Limpiar sesión para evitar bucles
            return redirect(url_for('main_views.landing_page'))


    num_total_missions = len(MISSIONS)
    is_final_mission = False
    mission_data_for_template = None

    mission_id_to_load = current_mission_id
    if mission_completed_show_results:
        mission_id_to_load = session.get('completed_mission_id_for_display', current_mission_id)
    
    mission_data_for_template = next((m for m in MISSIONS if m['id'] == mission_id_to_load), None)

    if not mission_completed_show_results and current_mission_id > num_total_missions:
        mission_data_for_template = {
            "id": current_mission_id, 
            "title": "Fin de la Demostración",
            "coordinator_message_subject": "Evaluación Concluida",
            "coordinator_message_body": "Ha completado todas las directivas asignadas en esta demostración. Su desempeño ha sido registrado. El futuro es... incierto.",
        }
        is_final_mission = True
    elif not mission_data_for_template and not is_final_mission: 
        flash(f"Error: Misión ID {mission_id_to_load} no encontrada.", "error")
        mission_data_for_template = { 
            "id": -1, "title": "Error de Sistema",
            "coordinator_message_subject": "Fallo en el Sistema de Misiones",
            "coordinator_message_body": "Contacte al administrador. Código de error: M_NOT_FOUND",
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
                           mission=mission_data_for_template,
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
    if current_mission_id > len(MISSIONS) and not session.get('mission_completed_show_results'): 
        flash("Ya ha completado todas las misiones disponibles.", "info")
        return redirect(url_for('main_views.game_interface'))

    current_mission = next((m for m in MISSIONS if m['id'] == current_mission_id), None)

    if not current_mission:
        flash("Error: No se pudo determinar la misión actual o ya ha finalizado.", "error")
        return redirect(url_for('main_views.game_interface'))

    session['mission_completed_show_results'] = False 

    restricted_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'CREATE', 'ALTER', 'GRANT', 'TRUNCATE', 'EXEC', 'PRAGMA']
    allow_restricted = current_mission.get("allow_restricted_keywords", False) 
    
    if not user_sql_query.upper().startswith("SELECT") and not allow_restricted:
        session['sql_error'] = "Comando no permitido. En esta fase, solo se permiten consultas SELECT."
        return redirect(url_for('main_views.game_interface'))
    
    if not allow_restricted:
        for keyword in restricted_keywords:
            # Mejorar la detección para evitar falsos positivos en strings dentro de SELECTs
            # Por ahora, una simplificación: si no es SELECT y contiene palabra clave, restringir.
            if not user_sql_query.upper().startswith("SELECT") and f" {keyword.upper()} " in f" {user_sql_query.upper()} ":
                session['sql_error'] = f"Comando '{keyword}' detectado y no permitido en esta misión."
                return redirect(url_for('main_views.game_interface'))

    user_query_results = None
    user_column_names = []
    is_correct = False
    eval_message = ""

    try:
        print(f"Ejecutando consulta del usuario para Misión {current_mission_id}: {user_sql_query}")
        user_result_proxy = db.session.execute(text(user_sql_query))
        
        if user_result_proxy.returns_rows:
            user_column_names = list(user_result_proxy.keys())
            user_query_results = [dict(row._mapping) for row in user_result_proxy.fetchall()]
        else: 
            db.session.commit() 
            user_query_results = [{"status": "Comando ejecutado, no se devolvieron filas."}] 
            user_column_names = ["status"]
            
        correct_query_text = current_mission['correct_query']
        print(f"Ejecutando consulta correcta para Misión {current_mission_id}: {correct_query_text}")
        correct_result_proxy = db.session.execute(text(correct_query_text))
        
        correct_column_names = list(correct_result_proxy.keys())
        correct_query_results = [dict(row._mapping) for row in correct_result_proxy.fetchall()]
        db.session.commit() 

        is_correct, eval_message = compare_results(
            user_results=user_query_results,
            user_columns=user_column_names,
            correct_results=correct_query_results,
            correct_columns=correct_column_names,
            eval_options=current_mission['evaluation_options']
        )
        
        session['query_results'] = user_query_results 
        session['column_names'] = user_column_names
        session.pop('sql_error', None) 

        if is_correct:
            flash(current_mission.get("success_message", "¡Consulta correcta!"), "success")
            session['mission_completed_show_results'] = True
            session['completed_mission_id_for_display'] = current_mission_id
            
            if current_mission_id == 3 and user_query_results: 
                 finding_summary = f"Misión {current_mission_id}: Anomalía detectada en PROYECTO_QUIMERA. {len(user_query_results)} registro(s) sospechoso(s) encontrado(s)."
                 if finding_summary not in session.get('archived_findings', []):
                     session.setdefault('archived_findings', []).append(finding_summary)
                 session.modified = True
        else: 
            flash(eval_message, "warning") 
            if current_mission.get("hint"):
                flash(f"PISTA: {current_mission['hint']}", "info")
                
    except exc.SQLAlchemyError as e: 
        db.session.rollback() 
        error_message = str(e.orig) if hasattr(e, 'orig') else str(e) 
        error_message_short = error_message.split('\n')[0]
        session['sql_error'] = f"Error de Sintaxis o Ejecución: {error_message_short}"
        session.pop('query_results', None) 
        session.pop('column_names', None)
        if current_mission and current_mission.get("hint"): 
            flash(f"PISTA: {current_mission['hint']}", "info")
    except Exception as e: 
        db.session.rollback()
        session['sql_error'] = f"Error inesperado al procesar la consulta: {str(e)}"
        session.pop('query_results', None)
        session.pop('column_names', None)
        print(f"Error inesperado en submit_query: {e}", exc_info=True) 

    return redirect(url_for('main_views.game_interface'))

@main_views.route('/next_mission', methods=['POST'])
def next_mission():
    current_mission_id = session.get('current_mission_id', 1)
    
    if session.get('mission_completed_show_results', False) and \
       session.get('completed_mission_id_for_display') == current_mission_id:
        
        if current_mission_id < len(MISSIONS): 
            session['current_mission_id'] = current_mission_id + 1
            flash("Nueva directiva recibida.", "info")
        else: 
            session['current_mission_id'] = current_mission_id + 1 
            flash("Todas las directivas han sido completadas. Evaluación finalizada.", "success")
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
    
    flash("Progreso de la simulación reiniciado. Volviendo a la primera directiva.", "info")
    return redirect(url_for('main_views.landing_page'))

# --- Rutas del Panel de Administrador ---
@main_views.route('/admin', methods=['GET'])
def admin_panel():
    """Muestra el panel de creación y gestión de misiones."""
    # Aquí podrías pasar datos existentes si estás editando una misión, etc.
    return render_template('admin_panel.html')

@main_views.route('/admin/execute_setup_sql', methods=['POST'])
def admin_execute_setup_sql():
    """Ejecuta el SQL de configuración y devuelve el resultado."""
    data = request.get_json()
    setup_sql_script = data.get('setup_sql', '')
    
    # Dividir el script en sentencias individuales (manejar punto y coma y saltos de línea)
    # Una forma simple es asumir que cada sentencia está separada por ; o es una línea no vacía.
    # Para mayor robustez, se podría usar una librería de parsing SQL, pero esto es un inicio.
    statements = [s.strip() for s in setup_sql_script.split(';') if s.strip()]
    if not statements and setup_sql_script.strip(): # Si no hay ; pero hay contenido, tomarlo como una sola sentencia
        statements = [setup_sql_script.strip()]
    
    if not statements:
        return jsonify({'error': 'No se proporcionaron sentencias SQL para ejecutar.'}), 400

    # Es CRUCIAL que esta ejecución sea en una sesión/transacción separada
    # o en una base de datos de prueba para no afectar la BD principal del juego
    # si el admin está probando. Para este ejemplo, usaremos la sesión actual,
    # pero en un sistema real, se necesitaría más aislamiento.
    try:
        # Aquí, en lugar de usar execute_sql_script directamente que hace commit,
        # podríamos querer probar sin commit o manejarlo con cuidado.
        # Por ahora, para simplicidad, lo usamos.
        # En un entorno real, el setup_sql del admin podría correr en una BD temporal.
        # O, si es la misma BD, asegurarse de que los DROPs y CREATEs sean seguros.
        
        # Para probar, podríamos querer limpiar tablas antes.
        # Esta es una simplificación. Una BD de prueba sería mejor.
        # db.session.execute(text("DROP TABLE IF EXISTS temp_test_table;")) # Ejemplo
        
        execute_sql_script(db.session, statements) # Esto hace commit
        return jsonify({'message': f'{len(statements)} sentencia(s) de configuración ejecutada(s) con éxito.'})
    except Exception as e:
        db.session.rollback() # Asegurar rollback si execute_sql_script no lo hizo o falló antes
        return jsonify({'error': f'Error al ejecutar SQL de configuración: {str(e)}'}), 500


@main_views.route('/admin/execute_correct_query', methods=['POST'])
def admin_execute_correct_query():
    """Ejecuta el SQL de configuración y luego la consulta correcta."""
    data = request.get_json()
    correct_query = data.get('correct_query', '')
    setup_sql_script = data.get('setup_sql', '') # Recibir el setup_sql para preparar el entorno

    if not correct_query:
        return jsonify({'error': 'No se proporcionó la consulta correcta.'}), 400
    
    if not correct_query.strip().upper().startswith("SELECT"):
        return jsonify({'error': 'La "Consulta Correcta" debe ser una sentencia SELECT.'}), 400

    setup_statements = [s.strip() for s in setup_sql_script.split(';') if s.strip()]
    if not setup_statements and setup_sql_script.strip():
        setup_statements = [setup_sql_script.strip()]

    try:
        # 1. Ejecutar el setup_sql para preparar el entorno de prueba
        if setup_statements:
            print(f"Admin: Ejecutando setup_sql ANTES de la consulta correcta: {len(setup_statements)} sentencias.")
            execute_sql_script(db.session, setup_statements) # Esto hace commit
        else:
            print("Admin: No hay setup_sql para ejecutar antes de la consulta correcta.")


        # 2. Ejecutar la consulta correcta
        print(f"Admin: Ejecutando consulta correcta: {correct_query}")
        result_proxy = db.session.execute(text(correct_query))
        
        if result_proxy.returns_rows:
            columns = list(result_proxy.keys())
            results = [dict(row._mapping) for row in result_proxy.fetchall()]
            db.session.commit() # Para cerrar la transacción SELECT
            return jsonify({'results': results, 'columns': columns})
        else:
            db.session.commit() # Para DML/DDL si se permitieran (aunque aquí se espera SELECT)
            return jsonify({'message': 'La consulta correcta se ejecutó pero no devolvió filas (o no era SELECT).'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al ejecutar la consulta correcta: {str(e)}'}), 500

@main_views.route('/admin/save_mission', methods=['POST'])
def save_mission():
    """Guarda la nueva misión (placeholder)."""
    try:
        mission_id = request.form.get('mission_id', type=int)
        mission_title = request.form.get('mission_title')
        mission_subject = request.form.get('mission_subject')
        mission_body = request.form.get('mission_body')
        mission_hint = request.form.get('mission_hint')
        mission_success_message = request.form.get('mission_success_message')
        
        setup_sql_script = request.form.get('setup_sql')
        correct_query_script = request.form.get('correct_query')
        
        # Las opciones de evaluación vienen como 'on' o None si son checkboxes
        order_matters = request.form.get('order_matters') == 'true'
        column_order_matters = request.form.get('column_order_matters') == 'true'
        check_column_names = request.form.get('check_column_names') == 'true'

        if not all([mission_id, mission_title, mission_subject, mission_body, mission_success_message, setup_sql_script, correct_query_script]):
            flash("Todos los campos principales de la misión son obligatorios.", "error")
            return redirect(url_for('main_views.admin_panel'))

        # Convertir setup_sql a lista de sentencias
        setup_sql_list = [s.strip() for s in setup_sql_script.split(';') if s.strip()]
        if not setup_sql_list and setup_sql_script.strip():
             setup_sql_list = [setup_sql_script.strip()]


        new_mission_data = {
            "id": mission_id,
            "title": mission_title,
            "coordinator_message_subject": mission_subject,
            "coordinator_message_body": mission_body,
            "setup_sql": setup_sql_list,
            "correct_query": correct_query_script,
            "evaluation_options": {
                'order_matters': order_matters,
                'column_order_matters': column_order_matters,
                'check_column_names': check_column_names
            },
            "hint": mission_hint,
            "success_message": mission_success_message
        }

        # Lógica para guardar la misión:
        # Opción 1: Si MISSIONS está en config.py, tendrías que modificar el archivo (no ideal para producción).
        # Opción 2: Si las misiones se guardan en una base de datos (ej. tabla MissionDefinitionDB),
        #           aquí crearías/actualizarías un registro en esa tabla.
        
        # Placeholder: Imprimir los datos y mostrar mensaje de éxito.
        print("Nueva misión para guardar:")
        import json
        print(json.dumps(new_mission_data, indent=2))
        
        # Simulación de guardado (añadir a la lista en memoria MISSIONS si es para prueba)
        # ¡¡¡ADVERTENCIA: Esto solo modifica la lista en memoria, no el archivo config.py!!!
        # Para persistencia real, necesitas guardar en un archivo o base de datos.
        
        # Verificar si el ID ya existe
        existing_mission = next((m for m in MISSIONS if m['id'] == mission_id), None)
        if existing_mission:
            # Actualizar misión existente (en memoria)
            MISSIONS[MISSIONS.index(existing_mission)] = new_mission_data
            flash(f"Misión ID {mission_id} actualizada en memoria con éxito.", "success")
        else:
            # Añadir nueva misión (en memoria)
            MISSIONS.append(new_mission_data)
            # Reordenar por ID para consistencia si se desea
            MISSIONS.sort(key=lambda m: m['id'])
            flash(f"Misión ID {mission_id} añadida en memoria con éxito.", "success")
        
        # print("MISSIONS actuales en memoria:", MISSIONS)

    except Exception as e:
        flash(f"Error al procesar el formulario de la misión: {str(e)}", "error")
        print(f"Error en save_mission: {e}", exc_info=True)

    return redirect(url_for('main_views.admin_panel'))
