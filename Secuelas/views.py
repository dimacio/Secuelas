from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from sqlalchemy import text, exc
from extensions import db
from config import MISSIONS

main_views = Blueprint('main_views', __name__)

print(f"Blueprint 'main_views' creado en views.py.")

@main_views.route('/game', methods=['GET'])
def game_interface():
    if 'current_mission_id' not in session:
        session['current_mission_id'] = 1
        session['archived_findings'] = []
        session['mission_completed_show_results'] = False

    current_mission_id = session['current_mission_id']
    mission_completed_show_results = session.get('mission_completed_show_results', False)
    
    # Pasamos la longitud de MISSIONS al template
    num_total_missions = len(MISSIONS)

    is_final_mission = False
    current_mission_data = None

    # Ajustamos la lógica para usar num_total_missions
    if not mission_completed_show_results and current_mission_id > num_total_missions: #
        current_mission_data = {
            "id": current_mission_id,
            "title": "Fin de la Demostración", #
            "coordinator_message_subject": "Evaluación Concluida", #
            "coordinator_message_body": "Ha completado todas las directivas asignadas en esta demostración. Su desempeño ha sido registrado. El futuro es... incierto.", #
        }
        is_final_mission = True #
    elif not mission_completed_show_results:
        current_mission_data = next((m for m in MISSIONS if m['id'] == current_mission_id), None) #

    if not mission_completed_show_results and not current_mission_data and not is_final_mission:
        flash("Error: Misión no encontrada.", "error") #
        current_mission_data = {
            "id": -1, #
            "title": "Error de Sistema", #
            "coordinator_message_subject": "Fallo en el Sistema de Misiones", #
            "coordinator_message_body": "Contacte al administrador. Código de error: M_NOT_FOUND", #
        }

    query_results = session.get('query_results', None)
    column_names = session.get('column_names', None)
    sql_error = session.get('sql_error', None)
    last_query = session.get('last_query', '')

    if not mission_completed_show_results:
        session.pop('query_results', None)
        session.pop('column_names', None)
        session.pop('sql_error', None)

    mission_to_template = current_mission_data if current_mission_data else {}
    
    if mission_completed_show_results:
        completed_mission_id = session.get('completed_mission_id_for_display', current_mission_id)
        # Aseguramos que mission_to_template tenga los datos de la misión que se está visualizando como completada
        mission_to_template = next((m for m in MISSIONS if m['id'] == completed_mission_id), mission_to_template)


    return render_template('index.html',
                           mission=mission_to_template,
                           results=query_results,
                           columns=column_names,
                           error=sql_error,
                           last_query=last_query,
                           archived_findings=session.get('archived_findings', []),
                           is_final_mission=is_final_mission,
                           mission_completed_show_results=mission_completed_show_results,
                           num_total_missions=num_total_missions) # <--- Añadir aquí

# ... (resto de views.py)

@main_views.route('/submit_query', methods=['POST'])
def submit_query():
    user_sql_query = request.form.get('sql_query', '')

    current_mission_id = session.get('current_mission_id', 1)
    if current_mission_id > len(MISSIONS):
         flash("Ya ha completado todas las misiones.", "info")
         return redirect(url_for('main_views.game_interface'))

    current_mission = next((m for m in MISSIONS if m['id'] == current_mission_id), None)

    if not current_mission:
        flash("Error: No se pudo determinar la misión actual o ya ha finalizado.", "error")
        return redirect(url_for('main_views.game_interface'))

    session['mission_completed_show_results'] = False # Resetear por si acaso

    restricted_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'CREATE', 'ALTER', 'GRANT', 'TRUNCATE']
    allow_restricted = current_mission.get("allow_restricted_keywords", False)

    if not allow_restricted and any(keyword in user_sql_query.upper() for keyword in restricted_keywords):
        session['sql_error'] = "Comando no permitido en esta fase de la simulación. Solo se permiten consultas de extracción de datos (SELECT)."
        session['last_query'] = user_sql_query
        return redirect(url_for('main_views.game_interface'))

    try:
        result_proxy = db.session.execute(text(user_sql_query))
        
        query_results = None
        column_names = []

        if result_proxy.returns_rows:
            column_names = list(result_proxy.keys())
            query_results = [dict(zip(column_names, row)) for row in result_proxy.fetchall()]
        else:
            db.session.commit()

        solution_correct = current_mission.get("solution_check") and current_mission["solution_check"](query_results)

        if solution_correct:
            flash(current_mission["success_message"], "success")
            session['mission_completed_show_results'] = True
            session['completed_mission_id_for_display'] = current_mission_id # Guardar ID de misión completada
            session['query_results'] = query_results # Guardar resultados para mostrar
            session['column_names'] = column_names   # Guardar columnas para mostrar
            session['last_query'] = user_sql_query   # Guardar la consulta exitosa para mostrar
            session.pop('sql_error', None)           # Limpiar cualquier error anterior

            # Lógica de "archivar" (se mantiene igual)
            # ... (tu lógica de archivado existente para misiones 3, 4, 5, 6)
            if current_mission_id == 3 and query_results:
                 finding_summary = f"Misión {current_mission_id}: Anomalía detectada en PROYECTO_QUIMERA. {len(query_results)} registro(s) sospechoso(s) encontrado(s)."
                 if finding_summary not in session['archived_findings']:
                     session['archived_findings'].append(finding_summary)
                 session.modified = True
            
            if current_mission_id == 4 and query_results:
                finding_summary = f"Misión {current_mission_id}: Personal con alta autorización identificado: {', '.join([r['name'] for r in query_results])}."
                if finding_summary not in session['archived_findings']:
                     session['archived_findings'].append(finding_summary)
                session.modified = True

            if current_mission_id == 5 and query_results:
                doc_token = query_results[0].get('document_token', 'N/A') if query_results and query_results[0] else 'N/A'
                finding_summary = f"Misión {current_mission_id}: Detalles del documento '{doc_token}' investigados y archivados."
                if finding_summary not in session['archived_findings']:
                     session['archived_findings'].append(finding_summary)
                session.modified = True
            
            if current_mission_id == 6 and query_results:
                finding_summary = f"Misión {current_mission_id}: Auditoría cruzada para 'PROYECTO_QUIMERA' realizada. {len(query_results)} accesos detallados."
                if finding_summary not in session['archived_findings']:
                     session['archived_findings'].append(finding_summary)
                session.modified = True
            # NO AVANZAMOS LA MISIÓN AQUÍ TODAVÍA
        else: # La solución no es correcta
            session['last_query'] = user_sql_query
            if query_results is not None:
                session['query_results'] = query_results
                session['column_names'] = column_names
            else: # Si no hubo resultados (ej. consulta vacía o comando sin retorno)
                session.pop('query_results', None) # Asegurar que no haya resultados viejos
                session.pop('column_names', None)


            if not session.get('sql_error'): 
                flash("La consulta se ejecutó, pero los resultados no cumplen el objetivo de la directiva. Revise su lógica o intente de nuevo.", "warning")
            if current_mission.get("hint"):
                flash(f"PISTA: {current_mission['hint']}", "info")
                
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        error_message = str(e).split('\n')[0]
        session['sql_error'] = f"Error de Sintaxis o Ejecución en la Consulta: {error_message}"
        session['last_query'] = user_sql_query
        session.pop('query_results', None) # Limpiar resultados en caso de error
        session.pop('column_names', None)
        if current_mission.get("hint"):
            flash(f"PISTA: {current_mission['hint']}", "info")
    except Exception as e: 
        db.session.rollback()
        session['sql_error'] = f"Error inesperado al procesar la consulta: {str(e)}"
        session['last_query'] = user_sql_query
        session.pop('query_results', None) # Limpiar resultados en caso de error
        session.pop('column_names', None)


    return redirect(url_for('main_views.game_interface'))

@main_views.route('/next_mission', methods=['POST']) # Es mejor POST para acciones que cambian estado
def next_mission():
    # Avanzar el ID de la misión
    current_mission_id = session.get('current_mission_id', 1)
    if current_mission_id <= len(MISSIONS):
        session['current_mission_id'] = current_mission_id + 1

    # Limpiar el estado de la misión completada y la consulta
    session['mission_completed_show_results'] = False
    session.pop('query_results', None)
    session.pop('column_names', None)
    session.pop('sql_error', None)
    session.pop('completed_mission_id_for_display', None)
    session['last_query'] = '' # Iniciar la nueva misión con el textarea vacío

    flash("Nueva directiva recibida.", "info")
    return redirect(url_for('main_views.game_interface'))

@main_views.route('/reset_progress')
def reset_progress():
    session.clear()
    flash("Progreso del juego reiniciado. Volviendo a la primera directiva.", "info")
    return redirect(url_for('main_views.game_interface'))