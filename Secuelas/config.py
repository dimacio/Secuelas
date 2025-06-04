# Secuelas/config.py
import datetime
import json # No es estrictamente necesario aquí si solo define datos Python

# --- Definiciones de Misiones (para carga inicial a la BD si está vacía) ---
# Esta lista se usará en init_db.py para poblar la tabla MissionDefinitionDB
# la primera vez o si la tabla está vacía.
# Una vez en la BD, la aplicación leerá de la BD.
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
        "setup_sql": [ # Esto se convertirá a un string separado por ';' para la BD
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
        "evaluation_options": { # Esto se convertirá a JSON string para la BD
            'order_matters': True,
            'column_order_matters': True,
            'check_column_names': True
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
        "setup_sql": [
            "DROP TABLE IF EXISTS employees;",
            "CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, department TEXT, position TEXT, security_clearance INTEGER, hire_date TEXT);",
            "INSERT INTO employees (id, name, department, position, security_clearance, hire_date) VALUES (1, 'Analista 734 (Usted)', 'Unidad de Escrutinio Informativo', 'Analista de Datos Jr.', 2, '2025-05-10');",
            "INSERT INTO employees (id, name, department, position, security_clearance, hire_date) VALUES (2, 'Supervisor Nex', 'Unidad de Escrutinio Informativo', 'Supervisor de Analistas', 3, '2023-02-15');",
            "INSERT INTO employees (id, name, department, position, security_clearance, hire_date) VALUES (3, 'Agente Externo K', 'Consultores Externos', 'Especialista en Seguridad de Datos', 4, '2024-11-01');",
            "INSERT INTO employees (id, name, department, position, security_clearance, hire_date) VALUES (4, 'Director General Umbra', 'Alta Dirección', 'Director General', 5, '2010-01-05');",
            "INSERT INTO employees (id, name, department, position, security_clearance, hire_date) VALUES (5, 'Técnico de Archivos Rho', 'Archivo Central', 'Archivista Principal', 2, '2018-07-22');"
        ],
        "correct_query": "SELECT id, name, department, position, security_clearance, hire_date FROM employees WHERE id = 2;",
        "evaluation_options": {
            'order_matters': True, 
            'column_order_matters': True,
            'check_column_names': True
        },
        "hint": "Necesitará seleccionar todas las columnas de la tabla 'employees' donde el 'id' sea igual a 2.",
        "success_message": "Datos del empleado ID 2 verificados y archivados. Proceda."
    },
    # ... (resto de las misiones definidas originalmente) ...
    # La misión del subte que creamos antes:
    {
        "id": 5, # Asegúrate de que el ID sea único y secuencial si es posible
        "title": "Investigación Subte Línea H",
        "coordinator_message_subject": "Alerta de Seguridad: Actividad Sospechosa Línea H",
        "coordinator_message_body": (
            "Se necesita encontrar los sospechosos de un posible atentado contra la autoridad reguladora de información médica.\n"
            "Se solicita consultar la base de datos de usuarios del subte línea H desde las 8 a las 9 horas del día 14 de junio de 2025."
        ),
        "setup_sql": [
            "DROP TABLE IF EXISTS subway_logs_linea_h;",
            "CREATE TABLE subway_logs_linea_h (log_id INTEGER PRIMARY KEY AUTOINCREMENT, card_id TEXT NOT NULL, entry_station TEXT NOT NULL, entry_timestamp TEXT NOT NULL, exit_station TEXT, exit_timestamp TEXT, passenger_details TEXT);",
            "INSERT INTO subway_logs_linea_h (card_id, entry_station, entry_timestamp, exit_station, exit_timestamp, passenger_details) VALUES ('SUBE001', 'Corrientes', '2025-06-14 07:30:00', 'Hospitales', '2025-06-14 07:55:00', 'Hombre con maletín, nervioso.');",
            "INSERT INTO subway_logs_linea_h (card_id, entry_station, entry_timestamp, exit_station, exit_timestamp, passenger_details) VALUES ('SUBE002', 'Once', '2025-06-14 08:05:00', 'Inclán', '2025-06-14 08:25:00', 'Mujer con sombrero grande, mirando constantemente a su alrededor.');",
            "INSERT INTO subway_logs_linea_h (card_id, entry_station, entry_timestamp, exit_station, exit_timestamp, passenger_details) VALUES ('SUBE003', 'Santa Fe', '2025-06-14 08:15:00', 'Caseros', '2025-06-14 08:40:00', 'Persona con capucha y gafas de sol.');",
            "INSERT INTO subway_logs_linea_h (card_id, entry_station, entry_timestamp, exit_station, exit_timestamp, passenger_details) VALUES ('SUBE004', 'Corrientes', '2025-06-14 08:30:00', 'Parque Patricios', '2025-06-14 08:55:00', 'Joven con mochila, parece apurado.');",
            "INSERT INTO subway_logs_linea_h (card_id, entry_station, entry_timestamp, exit_station, exit_timestamp, passenger_details) VALUES ('SUBE005', 'Humberto I', '2025-06-14 08:45:00', 'Corrientes', '2025-06-14 09:10:00', 'Pasajero regular, leyendo el diario.');", # Fuera de rango (09:10)
            "INSERT INTO subway_logs_linea_h (card_id, entry_station, entry_timestamp, exit_station, exit_timestamp, passenger_details) VALUES ('SUBE006', 'Inclán', '2025-06-14 08:58:00', 'Facultad de Derecho', '2025-06-14 09:20:00', 'Estudiante con libros.');",
            "INSERT INTO subway_logs_linea_h (card_id, entry_station, entry_timestamp, exit_station, exit_timestamp, passenger_details) VALUES ('SUBE007', 'Caseros', '2025-06-14 09:15:00', 'Once', '2025-06-14 09:35:00', 'Turista con cámara.');", # Fuera de rango
            "INSERT INTO subway_logs_linea_h (card_id, entry_station, entry_timestamp, exit_station, exit_timestamp, passenger_details) VALUES ('SUBE009', 'Corrientes', '2025-06-13 08:00:00', 'Hospitales', '2025-06-13 08:25:00', 'Pasajero del día anterior.');",
            "INSERT INTO subway_logs_linea_h (card_id, entry_station, entry_timestamp, exit_station, exit_timestamp, passenger_details) VALUES ('SUBE011', 'Facultad de Derecho', '2025-06-14 08:02:00', 'Corrientes', '2025-06-14 08:15:00', 'Abogado con portafolio.');"
        ],
        "correct_query": "SELECT log_id, card_id, entry_station, entry_timestamp, exit_station, exit_timestamp, passenger_details FROM subway_logs_linea_h WHERE entry_timestamp >= '2025-06-14 08:00:00' AND entry_timestamp <= '2025-06-14 09:00:00' ORDER BY entry_timestamp ASC;",
        "evaluation_options": {
            'order_matters': True,
            'column_order_matters': True,
            'check_column_names': True
        },
        "hint": "Filtre la tabla 'subway_logs_linea_h' por 'entry_timestamp' entre '2025-06-14 08:00:00' y '2025-06-14 09:00:00'.",
        "success_message": "Registros de la Línea H compilados para el período de interés."
    }
]
