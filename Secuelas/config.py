# Secuelas/config.py
import datetime

# --- Definiciones de Misiones ---
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
        # setup_sql se encarga de crear el esquema y los datos necesarios para ESTA misión.
        # Debería ser idempotente o limpiar tablas existentes si es necesario.
        "setup_sql": [
            "DROP TABLE IF EXISTS employees;",
            "DROP TABLE IF EXISTS documents;",
            "DROP TABLE IF EXISTS document_access_logs;",
            "CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, department TEXT, position TEXT, security_clearance INTEGER, hire_date TEXT);",
            "INSERT INTO employees (id, name, department, position, security_clearance, hire_date) VALUES (1, 'Analista 734 (Usted)', 'Unidad de Escrutinio Informativo', 'Analista de Datos Jr.', 2, '2025-05-10');",
            "INSERT INTO employees (id, name, department, position, security_clearance, hire_date) VALUES (2, 'Supervisor Nex', 'Unidad de Escrutinio Informativo', 'Supervisor de Analistas', 3, '2023-02-15');",
            "INSERT INTO employees (id, name, department, position, security_clearance, hire_date) VALUES (3, 'Agente Externo K', 'Consultores Externos', 'Especialista en Seguridad de Datos', 4, '2024-11-01');",
            "INSERT INTO employees (id, name, department, position, security_clearance, hire_date) VALUES (4, 'Director General Umbra', 'Alta Dirección', 'Director General', 5, '2010-01-05');",
            "INSERT INTO employees (id, name, department, position, security_clearance, hire_date) VALUES (5, 'Técnico de Archivos Rho', 'Archivo Central', 'Archivista Principal', 2, '2018-07-22');"
        ],
        "correct_query": "SELECT id, name, department, position, security_clearance, hire_date FROM employees WHERE department = 'Unidad de Escrutinio Informativo' ORDER BY id ASC;",
        "evaluation_options": {
            'order_matters': True,          # El orden de las filas importa
            'column_order_matters': True,   # El orden de las columnas importa
            'check_column_names': True      # Los nombres de las columnas deben coincidir
        },
        "hint": "Utilice SELECT para obtener columnas, FROM para especificar la tabla 'employees', y WHERE para filtrar por el departamento 'Unidad de Escrutinio Informativo'. Ordene por 'id'.",
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
        "setup_sql": [ # Mismo setup que la misión 1 para este ejemplo.
                       # En un escenario real, podrías tener setups diferentes o incrementales.
            "DROP TABLE IF EXISTS employees;",
            "CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, department TEXT, position TEXT, security_clearance INTEGER, hire_date TEXT);",
            "INSERT INTO employees (id, name, department, position, security_clearance, hire_date) VALUES (1, 'Analista 734 (Usted)', 'Unidad de Escrutinio Informativo', 'Analista de Datos Jr.', 2, '2025-05-10');",
            "INSERT INTO employees (id, name, department, position, security_clearance, hire_date) VALUES (2, 'Supervisor Nex', 'Unidad de Escrutinio Informativo', 'Supervisor de Analistas', 3, '2023-02-15');",
            "INSERT INTO employees (id, name, department, position, security_clearance, hire_date) VALUES (3, 'Agente Externo K', 'Consultores Externos', 'Especialista en Seguridad de Datos', 4, '2024-11-01');",
            "INSERT INTO employees (id, name, department, position, security_clearance, hire_date) VALUES (4, 'Director General Umbra', 'Alta Dirección', 'Director General', 5, '2010-01-05');",
            "INSERT INTO employees (id, name, department, position, security_clearance, hire_date) VALUES (5, 'Técnico de Archivos Rho', 'Archivo Central', 'Archivista Principal', 2, '2018-07-22');"
        ],
        # Se espera que el usuario seleccione todas las columnas.
        "correct_query": "SELECT id, name, department, position, security_clearance, hire_date FROM employees WHERE id = 2;",
        "evaluation_options": {
            'order_matters': True, # Solo una fila, así que el orden de filas es trivialmente verdadero
            'column_order_matters': True, # Para asegurar que seleccionen las columnas en el orden esperado o todas.
            'check_column_names': True
        },
        "hint": "Necesitará seleccionar todas las columnas de la tabla 'employees' donde el 'id' sea igual a 2.",
        "success_message": "Datos del empleado ID 2 verificados y archivados. Proceda."
    },
    {
        "id": 3,
        "title": "Auditoría de Acceso a Documentos Sensibles",
        "coordinator_message_subject": "Alerta de Seguridad Temporal – Revisión de Bitácora",
        "coordinator_message_body": (
            "Analista, se ha detectado una fluctuación anómala en los protocolos de acceso a documentos clasificados.\n"
            "Su tarea es auditar la bitácora 'document_access_logs'.\n"
            "Identifique y reporte todos los accesos al documento con token 'PROYECTO_QUIMERA' que hayan ocurrido después de las '2025-05-19 10:00:00'.\n"
            "Preste atención a cualquier detalle inusual."
        ),
        "setup_sql": [
            "DROP TABLE IF EXISTS employees;",
            "CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, department TEXT, position TEXT, security_clearance INTEGER, hire_date TEXT);",
            "INSERT INTO employees (id, name, department, position, security_clearance, hire_date) VALUES (1, 'Analista 734 (Usted)', 'Unidad de Escrutinio Informativo', 'Analista de Datos Jr.', 2, '2025-05-10');",
            "INSERT INTO employees (id, name, department, position, security_clearance, hire_date) VALUES (2, 'Supervisor Nex', 'Unidad de Escrutinio Informativo', 'Supervisor de Analistas', 3, '2023-02-15');",
            "INSERT INTO employees (id, name, department, position, security_clearance, hire_date) VALUES (3, 'Agente Externo K', 'Consultores Externos', 'Especialista en Seguridad de Datos', 4, '2024-11-01');",
            
            "DROP TABLE IF EXISTS documents;",
            "CREATE TABLE documents (id INTEGER PRIMARY KEY AUTOINCREMENT, document_token TEXT UNIQUE NOT NULL, title TEXT, classification_level INTEGER, creation_date TEXT);",
            "INSERT INTO documents (document_token, title, classification_level, creation_date) VALUES ('MANUAL_UEI_001', 'Manual de Orientación UEI', 1, '2025-01-10 00:00:00');",
            "INSERT INTO documents (document_token, title, classification_level, creation_date) VALUES ('PROYECTO_QUIMERA', 'Proyecto Quimera - Ultrasecreto', 5, '2024-06-15 00:00:00');",
            "INSERT INTO documents (document_token, title, classification_level, creation_date) VALUES ('REGISTRO_HISTORICO_77B', 'Registro Histórico 77B', 4, '2023-03-22 00:00:00');",

            "DROP TABLE IF EXISTS document_access_logs;",
            "CREATE TABLE document_access_logs (log_id INTEGER PRIMARY KEY AUTOINCREMENT, employee_id INTEGER, document_token_fk TEXT, access_timestamp TEXT, action TEXT, remarks TEXT, FOREIGN KEY (employee_id) REFERENCES employees(id), FOREIGN KEY (document_token_fk) REFERENCES documents(document_token));",
            "INSERT INTO document_access_logs (employee_id, document_token_fk, access_timestamp, action, remarks) VALUES (1, 'MANUAL_UEI_001', '2025-05-19 09:15:00', 'VIEW', 'Acceso estándar de orientación.');",
            "INSERT INTO document_access_logs (employee_id, document_token_fk, access_timestamp, action, remarks) VALUES (2, 'PROYECTO_QUIMERA', '2025-05-19 09:30:00', 'VIEW', 'Revisión de Supervisor.');", # Antes de las 10:00
            "INSERT INTO document_access_logs (employee_id, document_token_fk, access_timestamp, action, remarks) VALUES (3, 'PROYECTO_QUIMERA', '2025-05-19 11:05:30', 'CLASSIFIED_VIEW', 'Acceso no programado. Requiere seguimiento.');", # Después de las 10:00
            "INSERT INTO document_access_logs (employee_id, document_token_fk, access_timestamp, action, remarks) VALUES (1, 'PROYECTO_QUIMERA', '2025-05-19 14:20:00', 'VIEW', 'Acceso autorizado para tarea de auditoría.');" # Después de las 10:00
        ],
        "correct_query": "SELECT log_id, employee_id, document_token_fk, access_timestamp, action, remarks FROM document_access_logs WHERE document_token_fk = 'PROYECTO_QUIMERA' AND access_timestamp > '2025-05-19 10:00:00' ORDER BY log_id ASC;",
        "evaluation_options": {
            'order_matters': True,
            'column_order_matters': True,
            'check_column_names': True
        },
        "hint": "Consulte 'document_access_logs'. Filtre por 'document_token_fk' y 'access_timestamp'. Recuerde que las fechas/horas se comparan como texto en SQLite si no se usa formato ISO8601 completo o funciones de fecha.",
        "success_message": "Registros de acceso para 'PROYECTO_QUIMERA' compilados. Su diligencia es anotada."
    },
    # Agrega aquí el resto de las misiones, adaptándolas a esta nueva estructura.
    # Por ejemplo, Misión 4:
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
        "setup_sql": [ # Reutilizamos el setup de empleados de la misión 1
            "DROP TABLE IF EXISTS employees;",
            "CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, department TEXT, position TEXT, security_clearance INTEGER, hire_date TEXT);",
            "INSERT INTO employees (id, name, department, position, security_clearance, hire_date) VALUES (1, 'Analista 734 (Usted)', 'Unidad de Escrutinio Informativo', 'Analista de Datos Jr.', 2, '2025-05-10');",
            "INSERT INTO employees (id, name, department, position, security_clearance, hire_date) VALUES (2, 'Supervisor Nex', 'Unidad de Escrutinio Informativo', 'Supervisor de Analistas', 3, '2023-02-15');",
            "INSERT INTO employees (id, name, department, position, security_clearance, hire_date) VALUES (3, 'Agente Externo K', 'Consultores Externos', 'Especialista en Seguridad de Datos', 4, '2024-11-01');", # Clearance 4
            "INSERT INTO employees (id, name, department, position, security_clearance, hire_date) VALUES (4, 'Director General Umbra', 'Alta Dirección', 'Director General', 5, '2010-01-05');",      # Clearance 5
            "INSERT INTO employees (id, name, department, position, security_clearance, hire_date) VALUES (5, 'Técnico de Archivos Rho', 'Archivo Central', 'Archivista Principal', 2, '2018-07-22');"
        ],
        "correct_query": "SELECT id, name, department, position, security_clearance, hire_date FROM employees WHERE security_clearance > 3 ORDER BY id ASC;",
        "evaluation_options": {
            'order_matters': True,
            'column_order_matters': True,
            'check_column_names': True
        },
        "hint": "Consulte la tabla 'employees'. Filtre por la columna 'security_clearance' para valores mayores a 3. Ordene por 'id'.",
        "success_message": "Información obtenida. La discreción es su mejor aliada. Mantenga estos datos en reserva."
    }
]
