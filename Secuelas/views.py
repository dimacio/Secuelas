from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from sqlalchemy import text, exc
from extensions import db
from config import MISSIONS # MISSIONS se usa en game_interface

# Crear un Blueprint.
# El primer argumento es el nombre del Blueprint.
# El segundo es el nombre del módulo o paquete donde se encuentra el Blueprint (usualmente __name__).
main_views = Blueprint('main_views', __name__)

print(f"Blueprint 'main_views' creado en views.py.")

# Ruta raíz para una bienvenida o redirección (opcional)
@main_views.route('/')
def index():
    # Redirige directamente a la interfaz del juego en /game
    return redirect(url_for('main_views.game_interface'))

@main_views.route('/game', methods=['GET'])
def game_interface():
    """
    Maneja la lógica para mostrar la interfaz principal del juego,
    incluyendo la misión actual y los resultados de consultas anteriores.
    """
    if 'current_mission_id' not in session:
        session['current_mission_id'] = 1 # Empezar en la misión 1
        
        # Los "hallazgos" son resultados que se encontraron en busqueda anteriores.
        # Sería útil poner el nombre de alguna persona que accedio a un registro dudoso.
        # O el ID de un proyecto que no tiene ni nombre ni responsable asignado.
        session['archived_findings'] = [] # Para guardar "hallazgos"

    current_mission_id = session['current_mission_id']
    
    is_final_mission = False
    current_mission_data = None

    if current_mission_id > len(MISSIONS): # Si terminaste todas las misiones
        current_mission_data = {
            "id": current_mission_id, # Para consistencia con el template
            "title": "Fin de la Demostración",
            "coordinator_message_subject": "Evaluación Concluida",
            "coordinator_message_body": "Ha completado todas las directivas asignadas en esta demostración. Su desempeño ha sido registrado. El futuro es... incierto.",
        }
        is_final_mission = True
    else:
        current_mission_data = next((m for m in MISSIONS if m['id'] == current_mission_id), None)
        # is_final_mission permanece False si current_mission_data se encuentra

    if not current_mission_data and not is_final_mission: # Evitar sobreescribir el mensaje de fin de demo
        flash("Error: Misión no encontrada.", "error")
        current_mission_data = {
            "id": -1, # ID de error
            "title": "Error de Sistema",
            "coordinator_message_subject": "Fallo en el Sistema de Misiones",
            "coordinator_message_body": "Contacte al administrador. Código de error: M_NOT_FOUND",
        }

    query_results = session.pop('query_results', None)
    column_names = session.pop('column_names', None)
    sql_error = session.pop('sql_error', None)
    last_query = session.pop('last_query', '')
    
    # Asegurarse de que mission siempre tenga un valor para el template
    mission_to_template = current_mission_data if current_mission_data else {}

    return render_template('index.html', 
                           mission=mission_to_template,
                           results=query_results,
                           columns=column_names,
                           error=sql_error,
                           last_query=last_query,
                           archived_findings=session.get('archived_findings', []),
                           is_final_mission=is_final_mission)

@main_views.route('/submit_query', methods=['POST'])

def submit_query():
    """
    Procesa la consulta SQL enviada por el usuario, la ejecuta,
    verifica la solución de la misión y actualiza el estado del juego.
    """
    user_sql_query = request.form.get('sql_query', '') 
    session['last_query'] = user_sql_query
    
    current_mission_id = session.get('current_mission_id', 1)
    # Si ya se completaron las misiones, no procesar más consultas.
    if current_mission_id > len(MISSIONS):
         flash("Ya ha completado todas las misiones.", "info")
         return redirect(url_for('main_views.game_interface'))

    current_mission = next((m for m in MISSIONS if m['id'] == current_mission_id), None)

    if not current_mission:
        flash("Error: No se pudo determinar la misión actual o ya ha finalizado.", "error")
        return redirect(url_for('main_views.game_interface'))

    # Validación básica de palabras clave restringidas
    restricted_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'CREATE', 'ALTER', 'GRANT', 'TRUNCATE']
    allow_restricted = current_mission.get("allow_restricted_keywords", False) 

    if not allow_restricted and any(keyword in user_sql_query.upper() for keyword in restricted_keywords) :
        session['sql_error'] = "Comando no permitido en esta fase de la simulación. Solo se permiten consultas de extracción de datos (SELECT)."
        return redirect(url_for('main_views.game_interface'))

    try:
        # Ejecutar la consulta SQL del usuario
        result_proxy = db.session.execute(text(user_sql_query))
        
        query_results = None # Inicializar
        if result_proxy.returns_rows:
            column_names = list(result_proxy.keys())
            query_results = [dict(zip(column_names, row)) for row in result_proxy.fetchall()]
            session['query_results'] = query_results
            session['column_names'] = column_names
        else:
            # Para comandos que no devuelven filas (ej. DDL si se permitieran y ejecutaran correctamente)
            db.session.commit() 
            session['query_results'] = [{"status": "Comando ejecutado, no se devolvieron filas."}]
            session['column_names'] = ["status"]
            # query_results sigue siendo None o no relevante para solution_check si no devuelve filas

        # Chequear la solución de la misión
        solution_correct = current_mission.get("solution_check") and current_mission["solution_check"](query_results)

        if solution_correct:
            flash(current_mission["success_message"], "success")
            
            # Lógica de "archivar" para misiones específicas
            if current_mission_id == 3 and query_results:
                 finding_summary = f"Misión {current_mission_id}: Anomalía detectada en PROYECTO_QUIMERA. {len(query_results)} registro(s) sospechoso(s) encontrado(s)."
                 if finding_summary not in session['archived_findings']:
                     session['archived_findings'].append(finding_summary)
                 session.modified = True # Marcar la sesión como modificada
            
            if current_mission_id == 4 and query_results:
                finding_summary = f"Misión {current_mission_id}: Personal con alta autorización identificado: {', '.join([r['name'] for r in query_results])}."
                if finding_summary not in session['archived_findings']:
                     session['archived_findings'].append(finding_summary)
                session.modified = True

            # Avanzar a la siguiente misión si no se ha superado el total de misiones
            if session['current_mission_id'] <= len(MISSIONS):
                 session['current_mission_id'] += 1
        else: # La solución no es correcta
            # No mostrar este mensaje si ya hay un error de SQL (que se mostrará por separado)
            if not session.get('sql_error'): 
                flash("La consulta se ejecutó, pero los resultados no cumplen el objetivo de la directiva. Revise su lógica o intente de nuevo.", "warning")
            if current_mission.get("hint"):
                flash(f"PISTA: {current_mission['hint']}", "info")
                
    except exc.SQLAlchemyError as e:
        db.session.rollback() # Revertir en caso de error de BD
        error_message = str(e).split('\n')[0] # Tomar la primera línea del error para simplicidad
        session['sql_error'] = f"Error de Sintaxis o Ejecución en la Consulta: {error_message}"
        if current_mission.get("hint"): # Mostrar pista incluso si hay error de SQL
            flash(f"PISTA: {current_mission['hint']}", "info")
    except Exception as e:
        db.session.rollback()
        session['sql_error'] = f"Error inesperado al procesar la consulta: {str(e)}"

    return redirect(url_for('main_views.game_interface'))

@main_views.route('/reset_progress')
def reset_progress():
    """
    Reinicia el progreso del juego limpiando la sesión.
    """
    session.clear() # Limpia todas las variables de sesión
    flash("Progreso del juego reiniciado. Volviendo a la primera directiva.", "info")
    return redirect(url_for('main_views.game_interface'))
