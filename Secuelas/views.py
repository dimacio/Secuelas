# Secuelas/views.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from sqlalchemy import text, exc
from extensions import db
from config import MISSIONS  # Tus definiciones de misiones
from evaluation import compare_results  # Tu nueva función de evaluación
from init_db import execute_sql_script # Para configurar la BD de cada misión

main_views = Blueprint('main_views', __name__)

def setup_current_mission_db(mission_id):
    """Configura la base de datos para el mission_id dado usando su setup_sql."""
    current_mission = next((m for m in MISSIONS if m['id'] == mission_id), None)
    if current_mission and 'setup_sql' in current_mission:
        try:
            print(f"setup_current_mission_db: Configurando DB para Misión ID: {mission_id}")
            # Asegurar que se opera dentro del contexto de la aplicación
            with current_app.app_context():
                 execute_sql_script(db.session, current_mission['setup_sql'])
            print(f"setup_current_mission_db: DB configurada para Misión ID: {mission_id}")
            return True
        except Exception as e:
            # Usar flash para mostrar errores al usuario si es apropiado
            flash(f"Error crítico al configurar la base de datos para la misión: {e}", "error")
            print(f"setup_current_mission_db: Error crítico al configurar la base de datos para la misión {mission_id}: {e}")
            return False
    elif current_mission:
        print(f"setup_current_mission_db: No hay 'setup_sql' para la Misión ID: {mission_id}. Se asume que la DB está lista.")
        return True # No se necesita setup, proceder
    else:
        flash(f"Misión ID {mission_id} no encontrada para configuración de DB.", "error")
        print(f"setup_current_mission_db: Misión ID {mission_id} no encontrada.")
        return False

@main_views.route('/') # Ruta raíz para el juego
@main_views.route('/game', methods=['GET'])
def game_interface():
    if 'current_mission_id' not in session:
        session['current_mission_id'] = 1 # Empezar en la misión 1
        session['archived_findings'] = []
        # session['mission_completed_show_results'] = False # Se maneja más adelante

    current_mission_id = session.get('current_mission_id', 1)
    mission_completed_show_results = session.get('mission_completed_show_results', False)
    
    # Configurar la BD para la misión actual SI NO se están mostrando los resultados de una misión completada
    if not mission_completed_show_results:
        if not setup_current_mission_db(current_mission_id):
            # Si la configuración de la BD falla, es un problema serio.
            # game_interface debería probablemente mostrar un error y no la misión.
            # Por ahora, el error se flashea y la renderización continúa, lo que podría ser problemático.
            # Considerar renderizar una plantilla de error o redirigir.
            pass 

    num_total_missions = len(MISSIONS)
    is_final_mission = False
    mission_data_for_template = None

    # Determinar qué datos de misión mostrar
    mission_id_to_load = current_mission_id
    if mission_completed_show_results:
        mission_id_to_load = session.get('completed_mission_id_for_display', current_mission_id)
    
    mission_data_for_template = next((m for m in MISSIONS if m['id'] == mission_id_to_load), None)

    if not mission_completed_show_results and current_mission_id > num_total_missions:
        # Caso: Todas las misiones definidas han sido superadas
        mission_data_for_template = {
            "id": current_mission_id, # Podría ser un ID especial > num_total_missions
            "title": "Fin de la Demostración",
            "coordinator_message_subject": "Evaluación Concluida",
            "coordinator_message_body": "Ha completado todas las directivas asignadas en esta demostración. Su desempeño ha sido registrado. El futuro es... incierto.",
        }
        is_final_mission = True
    elif not mission_data_for_template and not is_final_mission: # Si no se encontró la misión a cargar
        flash(f"Error: Misión ID {mission_id_to_load} no encontrada.", "error")
        mission_data_for_template = { # Fallback
            "id": -1, "title": "Error de Sistema",
            "coordinator_message_subject": "Fallo en el Sistema de Misiones",
            "coordinator_message_body": "Contacte al administrador. Código de error: M_NOT_FOUND",
        }

    # Recuperar datos de la sesión para la plantilla
    query_results = session.get('query_results', None)
    column_names = session.get('column_names', None)
    sql_error = session.get('sql_error', None)
    last_query = session.get('last_query', '')

    # Limpiar resultados/errores de intentos anteriores si estamos cargando una nueva misión (no mostrando completada)
    if not mission_completed_show_results:
        session.pop('query_results', None)
        session.pop('column_names', None)
        session.pop('sql_error', None)
        # session['last_query'] = '' # Opcional: limpiar también la última consulta

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
    if current_mission_id > len(MISSIONS) and not session.get('mission_completed_show_results'): # Ya completó todo
        flash("Ya ha completado todas las misiones disponibles.", "info")
        return redirect(url_for('main_views.game_interface'))

    current_mission = next((m for m in MISSIONS if m['id'] == current_mission_id), None)

    if not current_mission:
        flash("Error: No se pudo determinar la misión actual o ya ha finalizado.", "error")
        return redirect(url_for('main_views.game_interface'))

    # La BD para esta misión ya debería estar configurada por la carga de game_interface.
    # Para mayor seguridad, se podría volver a llamar a setup_current_mission_db aquí,
    # pero podría ser redundante si la sesión y el flujo son correctos.
    # if not setup_current_mission_db(current_mission_id):
    #     return redirect(url_for('main_views.game_interface'))


    session['mission_completed_show_results'] = False # Resetear antes de procesar nueva consulta

    # Validación de palabras clave restringidas (simplificada)
    # Esta lógica puede necesitar ser más sofisticada si algunas misiones permiten ciertos comandos DDL/DML.
    restricted_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'CREATE', 'ALTER', 'GRANT', 'TRUNCATE', 'EXEC', 'PRAGMA']
    allow_restricted = current_mission.get("allow_restricted_keywords", False) # Futura opción por misión
    
    if not user_sql_query.upper().startswith("SELECT") and not allow_restricted:
        session['sql_error'] = "Comando no permitido. En esta fase, solo se permiten consultas SELECT."
        return redirect(url_for('main_views.game_interface'))
    
    # Chequeo más general de palabras clave si no es SELECT
    if not allow_restricted:
        for keyword in restricted_keywords:
            if keyword in user_sql_query.upper():
                # Podríamos ser más específicos, permitiendo SELECT que contengan sub-palabras como 'CREATE' en un string.
                # Este es un chequeo básico.
                if not user_sql_query.upper().startswith("SELECT"): # Solo restringir si no es un SELECT
                    session['sql_error'] = f"Comando '{keyword}' detectado y no permitido en esta misión."
                    return redirect(url_for('main_views.game_interface'))


    user_query_results = None
    user_column_names = []
    is_correct = False
    eval_message = ""

    try:
        # Ejecutar Consulta del Usuario
        print(f"Ejecutando consulta del usuario para Misión {current_mission_id}: {user_sql_query}")
        user_result_proxy = db.session.execute(text(user_sql_query))
        
        if user_result_proxy.returns_rows:
            user_column_names = list(user_result_proxy.keys())
            # Convertir RowProxy a dict para consistencia y facilidad de uso en la plantilla/evaluación
            user_query_results = [dict(row._mapping) for row in user_result_proxy.fetchall()]
        else: # Comando DML/DDL que no devuelve filas (ej. si se permitiera INSERT)
            db.session.commit() # Importante para que los cambios persistan
            user_query_results = [{"status": "Comando ejecutado, no se devolvieron filas."}] # Placeholder
            user_column_names = ["status"]
            # La evaluación actual está pensada para SELECT. Si se permiten DML,
            # la 'correct_query' debería ser un SELECT para verificar el estado,
            # y la lógica de 'compare_results' necesitaría adaptarse o el flujo aquí.

        # Ejecutar Consulta Correcta de la Misión (para comparación)
        correct_query_text = current_mission['correct_query']
        print(f"Ejecutando consulta correcta para Misión {current_mission_id}: {correct_query_text}")
        correct_result_proxy = db.session.execute(text(correct_query_text))
        
        correct_column_names = list(correct_result_proxy.keys())
        correct_query_results = [dict(row._mapping) for row in correct_result_proxy.fetchall()]
        db.session.commit() # Aunque sea SELECT, algunas DBs/drivers podrían necesitarlo o es buena práctica.

        # Comparar resultados
        is_correct, eval_message = compare_results(
            user_results=user_query_results,
            user_columns=user_column_names,
            correct_results=correct_query_results,
            correct_columns=correct_column_names,
            eval_options=current_mission['evaluation_options']
        )
        
        session['query_results'] = user_query_results # Guardar para mostrar siempre
        session['column_names'] = user_column_names
        session.pop('sql_error', None) # Limpiar error si la consulta se ejecutó

        if is_correct:
            flash(current_mission.get("success_message", "¡Consulta correcta!"), "success")
            session['mission_completed_show_results'] = True
            session['completed_mission_id_for_display'] = current_mission_id
            
            # Lógica de archivado
            if current_mission_id == 3 and user_query_results: # Ejemplo para misión 3
                 finding_summary = f"Misión {current_mission_id}: Anomalía detectada en PROYECTO_QUIMERA. {len(user_query_results)} registro(s) sospechoso(s) encontrado(s)."
                 if finding_summary not in session.get('archived_findings', []):
                     session.setdefault('archived_findings', []).append(finding_summary)
                 session.modified = True
            # Añadir más lógica de archivado para otras misiones si es necesario

        else: # Solución incorrecta
            flash(eval_message, "warning") # Mostrar el mensaje de la función de evaluación
            if current_mission.get("hint"):
                flash(f"PISTA: {current_mission['hint']}", "info")
                
    except exc.SQLAlchemyError as e: # Errores de DB (sintaxis, etc.)
        db.session.rollback() # Revertir cualquier transacción parcial
        error_message = str(e.orig) if hasattr(e, 'orig') else str(e) # Mensaje de error más específico
        error_message_short = error_message.split('\n')[0]
        session['sql_error'] = f"Error de Sintaxis o Ejecución: {error_message_short}"
        session.pop('query_results', None) # Limpiar resultados en caso de error
        session.pop('column_names', None)
        if current_mission and current_mission.get("hint"): # Asegurar que current_mission existe
            flash(f"PISTA: {current_mission['hint']}", "info")
    except Exception as e: # Otros errores inesperados
        db.session.rollback()
        session['sql_error'] = f"Error inesperado al procesar la consulta: {str(e)}"
        session.pop('query_results', None)
        session.pop('column_names', None)
        print(f"Error inesperado en submit_query: {e}", exc_info=True) # Loggear el traceback completo

    return redirect(url_for('main_views.game_interface'))

@main_views.route('/next_mission', methods=['POST'])
def next_mission():
    current_mission_id = session.get('current_mission_id', 1)
    
    # Solo avanzar si la misión actual fue marcada como completada y mostrada
    if session.get('mission_completed_show_results', False) and \
       session.get('completed_mission_id_for_display') == current_mission_id:
        
        if current_mission_id < len(MISSIONS): # Si hay más misiones
            session['current_mission_id'] = current_mission_id + 1
            flash("Nueva directiva recibida.", "info")
        else: # Era la última misión
            session['current_mission_id'] = current_mission_id + 1 # Ir a estado "post-final"
            flash("Todas las directivas han sido completadas. Evaluación finalizada.", "success")
    else:
        # No debería llegar aquí si el botón "Siguiente Directiva" solo aparece tras completar.
        # Pero si llega, no avanzar y quizás mostrar un mensaje.
        flash("Complete la directiva actual antes de continuar.", "warning")


    # Limpiar estado para la nueva misión (o para reintentar la actual si no se avanzó)
    session['mission_completed_show_results'] = False
    session.pop('query_results', None)
    session.pop('column_names', None)
    session.pop('sql_error', None)
    session.pop('completed_mission_id_for_display', None)
    session['last_query'] = '' # Empezar la nueva misión con el área de texto vacía

    return redirect(url_for('main_views.game_interface'))

@main_views.route('/reset_progress')
def reset_progress():
    # Guardar hallazgos si se quiere persistir algo entre reinicios totales, o limpiar todo.
    # Por ahora, limpia todo relacionado con el progreso de la misión.
    session.pop('current_mission_id', None)
    session.pop('archived_findings', None) # Opcional, decidir si se reinician los hallazgos
    session.pop('mission_completed_show_results', None)
    session.pop('query_results', None)
    session.pop('column_names', None)
    session.pop('sql_error', None)
    session.pop('last_query', None)
    session.pop('completed_mission_id_for_display', None)
    
    flash("Progreso de la simulación reiniciado. Volviendo a la primera directiva.", "info")
    return redirect(url_for('main_views.game_interface'))
