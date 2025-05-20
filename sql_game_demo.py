import os
from flask import Flask, render_template_string, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, exc
import datetime

# --- Configuración de la Aplicación Flask ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_super_secreta_llave_aqui_cambiala' # Cambia esto por una llave secreta real
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Base de datos en memoria para el demo
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Modelos de la Base de Datos (SQLAlchemy) ---
class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100))
    security_clearance = db.Column(db.Integer, default=1)
    hire_date = db.Column(db.Date)

    def __repr__(self):
        return f'<Employee {self.id}: {self.name}>'

class DocumentAccessLog(db.Model):
    __tablename__ = 'document_access_logs'
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    document_id = db.Column(db.String(50))
    access_timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    action = db.Column(db.String(50)) # e.g., 'VIEW', 'EDIT', 'CLASSIFIED_VIEW'
    remarks = db.Column(db.String(255), nullable=True)

    employee = db.relationship('Employee', backref=db.backref('access_logs', lazy=True))

    def __repr__(self):
        return f'<Log {self.log_id} by Employee {self.employee_id} on Doc {self.document_id}>'

# --- Datos Iniciales y Misiones ---
MISSIONS = [
    {
        "id": 1,
        "title": "Orientación Inicial",
        "coordinator_message_subject": "Directiva de Incorporación 001-A",
        "coordinator_message_body": (
            "Analista, bienvenido a la Unidad de Escrutinio Informativo (UEI).\n"
            "Su primera directiva es familiarizarse con el personal asignado a esta Unidad.\n"
            "Presente un listado completo de todos los empleados de la 'Unidad de Escrutinio Informativo'."
        ),
        "expected_table": "employees",
        "solution_check": lambda results: (
            results is not None and
            len(results) == 2 and
            all(row['department'] == 'Unidad de Escrutinio Informativo' for row in results) and
            any(row['name'] == 'Analista 734 (Usted)' for row in results) and
            any(row['name'] == 'Coordinador Primus' for row in results)
        ),
        "hint": "Utilice SELECT para obtener columnas, FROM para especificar la tabla 'employees', y WHERE para filtrar por el departamento 'Unidad de Escrutinio Informativo'.",
        "success_message": "Registro aceptado. Su familiarización inicial ha sido procesada."
    },
    {
        "id": 2,
        "title": "Verificación de Credenciales",
        "coordinator_message_subject": "Solicitud de Información Confidencial R-002",
        "coordinator_message_body": (
            "Analista, se requiere una verificación urgente de las credenciales del empleado con ID 2.\n"
            "Extraiga y presente el registro completo de dicho individuo."
        ),
        "expected_table": "employees",
        "solution_check": lambda results: (
            results is not None and
            len(results) == 1 and
            results[0]['id'] == 2 and
            results[0]['name'] == 'Supervisor Nex'
        ),
        "hint": "Necesitará seleccionar todas las columnas (*) de la tabla 'employees' donde el 'id' sea igual a 2.",
        "success_message": "Datos del empleado ID 2 verificados y archivados. Proceda."
    },
    {
        "id": 3,
        "title": "Auditoría de Acceso a Documentos Sensibles",
        "coordinator_message_subject": "Alerta de Seguridad Temporal – Revisión de Bitácora",
        "coordinator_message_body": (
            "Analista, se ha detectado una fluctuación anómala en los protocolos de acceso a documentos clasificados.\n"
            "Su tarea es auditar la bitácora 'document_access_logs'.\n"
            "Identifique y reporte todos los accesos al documento 'PROYECTO_QUIMERA' que hayan ocurrido después de las 10:00:00 del 2025-05-19.\n"
            "Preste atención a cualquier detalle inusual."
        ),
        "expected_table": "document_access_logs",
        "solution_check": lambda results: (
            results is not None and
            len(results) >= 1 and # Podría haber más de uno, pero al menos el sospechoso
            any(row['document_id'] == 'PROYECTO_QUIMERA' and 
                datetime.datetime.strptime(row['access_timestamp'].split('.')[0], '%Y-%m-%d %H:%M:%S') > datetime.datetime(2025, 5, 19, 10, 0, 0) and
                row['employee_id'] == 3 # El acceso del "Agente Externo"
                for row in results)
        ),
        "hint": "Consulte la tabla 'document_access_logs'. Filtre por 'document_id' y 'access_timestamp'. Recuerde que las fechas y horas deben compararse cuidadosamente.",
        "success_message": "Registros de acceso para 'PROYECTO_QUIMERA' compilados. Su diligencia es anotada. Una entrada parece... peculiar. Archive este hallazgo para referencia futura."
    },
    {
        "id": 4,
        "title": "El Contacto Misterioso",
        "coordinator_message_subject": "Mensaje Interceptado - Canal Seguro 7",
        "coordinator_message_body": (
            "Una nueva comunicación ha llegado a su terminal. Parece encriptada, pero el remitente es desconocido.\n"
            "REMITENTE: 'Observador Silencioso'\n"
            "MENSAJE: 'Analista 734. Sus habilidades son... prometedoras. Hay verdades ocultas en los datos que manipula.\n"
            "Busque en los registros de empleados a aquellos con un nivel de autorización de seguridad ('security_clearance') superior a 3. "
            "No todos los que vigilan son guardianes de la verdad. Tenga cuidado.'"
        ),
        "expected_table": "employees",
        "solution_check": lambda results: (
            results is not None and
            len(results) == 1 and
            results[0]['name'] == 'Director General Umbra' and
            results[0]['security_clearance'] == 5
        ),
        "hint": "Consulte la tabla 'employees'. Filtre por la columna 'security_clearance' para valores mayores a 3.",
        "success_message": "Información obtenida. La discreción es su mejor aliada. Mantenga estos datos en reserva."
    }
]

# --- Funciones Auxiliares ---
def initialize_database():
    """Crea las tablas y carga los datos iniciales."""
    with app.app_context():
        db.create_all()

        # Datos iniciales para empleados
        if not Employee.query.first():
            employees_data = [
                Employee(id=1, name="Analista 734 (Usted)", department="Unidad de Escrutinio Informativo", position="Analista de Datos Jr.", security_clearance=2, hire_date=datetime.date(2025, 5, 10)),
                Employee(id=2, name="Supervisor Nex", department="Unidad de Escrutinio Informativo", position="Supervisor de Analistas", security_clearance=3, hire_date=datetime.date(2023, 2, 15)),
                Employee(id=3, name="Agente Externo K", department="Consultores Externos", position="Especialista en Seguridad de Datos", security_clearance=4, hire_date=datetime.date(2024, 11, 1)),
                Employee(id=4, name="Director General Umbra", department="Alta Dirección", position="Director General", security_clearance=5, hire_date=datetime.date(2010, 1, 5)),
                Employee(id=5, name="Técnico de Archivos Rho", department="Archivo Central", position="Archivista Principal", security_clearance=2, hire_date=datetime.date(2018, 7, 22)),
            ]
            db.session.bulk_save_objects(employees_data)
            db.session.commit()
        
        # Datos iniciales para registros de acceso a documentos
        if not DocumentAccessLog.query.first():
            # Asegurarse que las fechas son correctas para la misión 3
            # Usar datetime.datetime para access_timestamp
            # Para SQLite, las fechas y horas se almacenan como cadenas ISO8601
            
            access_logs_data = [
                DocumentAccessLog(employee_id=1, document_id="MANUAL_UEI_001", action="VIEW", access_timestamp=datetime.datetime(2025, 5, 19, 9, 15, 0), remarks="Acceso estándar de orientación."),
                DocumentAccessLog(employee_id=2, document_id="PROYECTO_QUIMERA", action="VIEW", access_timestamp=datetime.datetime(2025, 5, 19, 9, 30, 0), remarks="Revisión de Supervisor."),
                DocumentAccessLog(employee_id=5, document_id="REGISTRO_HISTORICO_77B", action="ARCHIVE", access_timestamp=datetime.datetime(2025, 5, 19, 9, 45, 0)),
                # Este es el registro anómalo para la misión 3
                DocumentAccessLog(employee_id=3, document_id="PROYECTO_QUIMERA", action="CLASSIFIED_VIEW", access_timestamp=datetime.datetime(2025, 5, 19, 11, 5, 30), remarks="Acceso no programado. Requiere seguimiento."),
                DocumentAccessLog(employee_id=1, document_id="PROYECTO_QUIMERA", action="VIEW", access_timestamp=datetime.datetime(2025, 5, 19, 14, 20, 0), remarks="Acceso autorizado para tarea de auditoría."),
                DocumentAccessLog(employee_id=4, document_id="PROYECTO_QUIMERA", action="VIEW", access_timestamp=datetime.datetime(2025, 5, 18, 17, 0, 0), remarks="Revisión Directiva."),
            ]
            db.session.bulk_save_objects(access_logs_data)
            db.session.commit()

# --- Rutas de la Aplicación (Flask Endpoints) ---
@app.route('/', methods=['GET'])
def game_interface():
    if 'current_mission_id' not in session:
        session['current_mission_id'] = 1 # Empezar en la misión 1
        session['archived_findings'] = [] # Para guardar "hallazgos"

    current_mission_id = session['current_mission_id']
    
    if current_mission_id > len(MISSIONS):
        # Todas las misiones completadas
        current_mission_data = {
            "title": "Fin de la Demostración",
            "coordinator_message_subject": "Evaluación Concluida",
            "coordinator_message_body": "Ha completado todas las directivas asignadas en esta demostración. Su desempeño ha sido registrado. El futuro es... incierto.",
        }
        is_final_mission = True
    else:
        current_mission_data = next((m for m in MISSIONS if m['id'] == current_mission_id), None)
        is_final_mission = False

    if not current_mission_data:
        # Si por alguna razón no se encuentra la misión (debería ser el caso de fin de demo)
        flash("Error: Misión no encontrada o demostración finalizada.", "error")
        # Podríamos redirigir a algún sitio o mostrar un mensaje final genérico.
        # Para este demo, si current_mission_id > len(MISSIONS), ya se maneja arriba.
        # Si es otro error, mostramos la interfaz con el error.
        current_mission_data = { # Fallback
            "title": "Error de Sistema",
            "coordinator_message_subject": "Fallo en el Sistema de Misiones",
            "coordinator_message_body": "Contacte al administrador. Código de error: M_NOT_FOUND",
        }


    query_results = session.pop('query_results', None)
    column_names = session.pop('column_names', None)
    sql_error = session.pop('sql_error', None)
    last_query = session.pop('last_query', '')
    
    return render_template_string(HTML_TEMPLATE, 
                                  mission=current_mission_data,
                                  results=query_results,
                                  columns=column_names,
                                  error=sql_error,
                                  last_query=last_query,
                                  archived_findings=session.get('archived_findings', []),
                                  is_final_mission=is_final_mission)

@app.route('/submit_query', methods=['POST'])
def submit_query():
    user_sql_query = request.form.get('sql_query', '')
    session['last_query'] = user_sql_query
    
    current_mission_id = session.get('current_mission_id', 1)
    current_mission = next((m for m in MISSIONS if m['id'] == current_mission_id), None)

    if not current_mission:
        flash("Error: No se pudo determinar la misión actual.", "error")
        return redirect(url_for('game_interface'))

    # --- ¡ADVERTENCIA DE SEGURIDAD IMPORTANTE! ---
    # Ejecutar SQL directamente desde la entrada del usuario es EXTREMADAMENTE PELIGROSO
    # en una aplicación real. Esto puede llevar a inyecciones SQL.
    # Para un juego de aprendizaje, se necesita un entorno MUY controlado o un parser de SQL.
    # Este demo lo hace de forma simplificada y con riesgos. NO USAR EN PRODUCCIÓN.
    # Se recomienda limitar los tipos de comandos permitidos (ej. solo SELECT).
    
    # Validación básica (muy simplificada)
    restricted_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'CREATE', 'ALTER', 'GRANT', 'TRUNCATE']
    if any(keyword in user_sql_query.upper() for keyword in restricted_keywords) and current_mission_id < 100: # Misiones futuras podrían permitirlo
        session['sql_error'] = "Comando no permitido en esta fase de la simulación. Solo se permiten consultas de extracción de datos (SELECT)."
        return redirect(url_for('game_interface'))

    try:
        # Usar text() para indicar a SQLAlchemy que es una consulta SQL literal.
        # SQLAlchemy intentará parametrizar si encuentra placeholders estilo :param,
        # pero aquí estamos ejecutando la consulta completa del usuario.
        result_proxy = db.session.execute(text(user_sql_query))
        
        # Para SELECT, obtener resultados y nombres de columnas
        if result_proxy.returns_rows:
            column_names = list(result_proxy.keys())
            query_results = [dict(zip(column_names, row)) for row in result_proxy.fetchall()]
            session['query_results'] = query_results
            session['column_names'] = column_names
        else:
            # Para comandos que no devuelven filas (ej. DDL si se permitieran)
            db.session.commit() # Necesario para que cambios como UPDATE/INSERT (si se permitieran) persistan
            session['query_results'] = [{"status": "Comando ejecutado, no se devolvieron filas."}]
            session['column_names'] = ["status"]


        # Chequear la solución de la misión
        if current_mission.get("solution_check") and current_mission["solution_check"](query_results if result_proxy.returns_rows else None):
            flash(current_mission["success_message"], "success")
            
            # Lógica de "archivar" para la misión 3 y 4 (o cualquier misión que lo requiera)
            if current_mission_id == 3 and query_results:
                 # Podríamos ser más específicos sobre qué archivar
                finding_summary = f"Misión {current_mission_id}: Anomalía detectada en PROYECTO_QUIMERA. {len(query_results)} registro(s) sospechoso(s) encontrado(s)."
                if finding_summary not in session['archived_findings']:
                     session['archived_findings'].append(finding_summary)
                session.modified = True # Marcar la sesión como modificada
            
            if current_mission_id == 4 and query_results:
                finding_summary = f"Misión {current_mission_id}: Personal con alta autorización identificado: {', '.join([r['name'] for r in query_results])}."
                if finding_summary not in session['archived_findings']:
                     session['archived_findings'].append(finding_summary)
                session.modified = True


            if session['current_mission_id'] <= len(MISSIONS):
                 session['current_mission_id'] += 1
        else:
            flash("La consulta se ejecutó, pero los resultados no cumplen el objetivo de la directiva. Revise su lógica o intente de nuevo.", "warning")
            if current_mission.get("hint"):
                flash(f"PISTA: {current_mission['hint']}", "info")
                
    except exc.SQLAlchemyError as e:
        db.session.rollback() # Revertir en caso de error
        # Formatear el error para que sea más legible (simplificado)
        error_message = str(e).split('\n')[0] # Tomar la primera línea del error
        session['sql_error'] = f"Error de Sintaxis o Ejecución en la Consulta: {error_message}"
        if current_mission.get("hint"):
            flash(f"PISTA: {current_mission['hint']}", "info")
    except Exception as e:
        db.session.rollback()
        session['sql_error'] = f"Error inesperado al procesar la consulta: {str(e)}"

    return redirect(url_for('game_interface'))

@app.route('/reset_progress')
def reset_progress():
    session.pop('current_mission_id', None)
    session.pop('archived_findings', None)
    session.pop('query_results', None)
    session.pop('column_names', None)
    session.pop('sql_error', None)
    session.pop('last_query', None)
    flash("Progreso del juego reiniciado. Volviendo a la primera directiva.", "info")
    return redirect(url_for('game_interface'))

# --- Plantilla HTML (embebida para simplicidad del demo) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UEI - Terminal de Analista</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { font-family: 'Courier New', Courier, monospace; background-color: #0A0A0A; color: #00FF41; }
        .terminal-container { border: 2px solid #00FF41; padding: 20px; margin: 20px; background-color: #0D0D0D; box-shadow: 0 0 15px #00FF41; }
        .message-box { border: 1px solid #00B32C; padding: 15px; margin-bottom: 20px; background-color: #0F0F0F; }
        .console-input { width: 100%; background-color: #000; color: #00FF41; border: 1px solid #00B32C; padding: 10px; font-family: 'Courier New', Courier, monospace; margin-bottom:10px; }
        .results-table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        .results-table th, .results-table td { border: 1px solid #00B32C; padding: 8px; text-align: left; }
        .results-table th { background-color: #00330D; }
        .btn { background-color: #005010; color: #00FF41; border: 1px solid #00FF41; padding: 8px 15px; cursor: pointer; margin-top:10px; }
        .btn:hover { background-color: #007717; }
        .flash-message { padding: 10px; margin-bottom: 15px; border: 1px solid; }
        .flash-success { background-color: #004d00; color: #ccffcc; border-color: #009900; }
        .flash-warning { background-color: #4d4d00; color: #ffffcc; border-color: #999900; }
        .flash-error { background-color: #4d0000; color: #ffcccc; border-color: #990000; }
        .flash-info { background-color: #00334d; color: #cce6ff; border-color: #006699; }
        .archived-findings { margin-top: 20px; border-top: 1px dashed #00B32C; padding-top: 15px; }
        .archived-findings h3 { color: #00FF41; }
        .archived-findings ul { list-style-type: '> '; padding-left: 20px; }
    </style>
</head>
<body class="p-4">
    <div class="terminal-container">
        <header class="mb-6">
            <h1 class="text-3xl text-center border-b-2 border-[#00FF41] pb-2">TERMINAL DE ANALISTA - UNIDAD DE ESCRUTINIO INFORMATIVO</h1>
            <p class="text-sm text-center mt-1">PROTOCOLO DE SEGURIDAD {{ mission.id if mission else 'N/A' }} ACTIVADO</p>
        </header>

        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="flash-message flash-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        {% if mission %}
            <section id="mission-briefing" class="message-box">
                <h2 class="text-xl font-bold mb-2">[DIRECTIVA ACTUAL: {{ mission.title }}]</h2>
                <p class="text-sm mb-1"><strong>ASUNTO:</strong> {{ mission.coordinator_message_subject }}</p>
                <hr class="border-[#00B32C] my-2">
                <div class="whitespace-pre-wrap">{{ mission.coordinator_message_body }}</div>
            </section>
            
            {% if not is_final_mission %}
            <section id="sql-console">
                <h3 class="text-lg mb-2">ENTRADA DE CONSULTA SQL:</h3>
                <form action="{{ url_for('submit_query') }}" method="POST">
                    <textarea name="sql_query" class="console-input" rows="8" placeholder="Escriba su consulta SQL aquí...">{{ last_query if last_query else '' }}</textarea>
                    <button type="submit" class="btn">EJECUTAR CONSULTA</button>
                </form>
            </section>
            {% endif %}
        {% else %}
            <p class="text-red-500">Error: No se pudo cargar la misión actual.</p>
        {% endif %}

        {% if error %}
            <section id="error-output" class="mt-4 p-3 bg-red-900 border border-red-500">
                <h3 class="text-lg text-red-300">ERROR DE SISTEMA:</h3>
                <p class="text-red-200 whitespace-pre-wrap">{{ error }}</p>
            </section>
        {% endif %}

        {% if results %}
            <section id="query-results" class="mt-4">
                <h3 class="text-lg mb-2">RESULTADOS DE LA CONSULTA:</h3>
                {% if columns and results %}
                    <div class="overflow-x-auto">
                        <table class="results-table">
                            <thead>
                                <tr>
                                    {% for col_name in columns %}
                                        <th>{{ col_name }}</th>
                                    {% endfor %}
                                </tr>
                            </thead>
                            <tbody>
                                {% for row in results %}
                                    <tr>
                                        {% for col_name in columns %}
                                            <td>{{ row[col_name] }}</td>
                                        {% endfor %}
                                    </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                {% else %}
                    <p>La consulta no produjo resultados visibles o fue un comando sin retorno de filas.</p>
                {% endif %}
            </section>
        {% endif %}
        
        {% if archived_findings %}
        <section class="archived-findings">
            <h3>HALLAZGOS ARCHIVADOS PARA REFERENCIA FUTURA:</h3>
            <ul>
                {% for finding in archived_findings %}
                    <li>{{ finding }}</li>
                {% endfor %}
            </ul>
        </section>
        {% endif %}

        <footer class="mt-8 pt-4 border-t-2 border-[#00FF41] text-center">
            <a href="{{ url_for('reset_progress') }}" class="btn bg-yellow-700 border-yellow-500 text-yellow-200 hover:bg-yellow-600">REINICIAR SIMULACIÓN</a>
            <p class="text-xs mt-3">Departamento de Control Interno - Todos los accesos son monitoreados.</p>
        </footer>
    </div>
</body>
</html>
"""

# --- Inicialización y Ejecución ---
if __name__ == '__main__':
    with app.app_context():
        # Eliminar la base de datos si existe para asegurar un estado limpio en cada ejecución del demo
        if os.path.exists('instance/memory.db'): # Flask por defecto crea una carpeta 'instance' para sqlite si no es :memory:
            os.remove('instance/memory.db') # Esto es más para un archivo físico, :memory: se reinicia sola.
        
        initialize_database() # Crea tablas y datos si no existen (para :memory:, siempre se crean)
    
    # app.run(debug=True) # debug=True es útil para desarrollo
    app.run(debug=True, host='0.0.0.0', port=5001) # Para que sea accesible en la red local si es necesario

