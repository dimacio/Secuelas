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
            "DROP TABLE IF EXISTS products;",
            "DROP TABLE IF EXISTS orders;",
            "DROP TABLE IF EXISTS users;",
            "DROP TABLE IF EXISTS employees_corp;",
            "DROP TABLE IF EXISTS departments_corp;",
            "DROP TABLE IF EXISTS subway_logs_linea_h;",
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
            "DROP TABLE IF EXISTS documents;",
            "DROP TABLE IF EXISTS document_access_logs;",
            "DROP TABLE IF EXISTS products;",
            "DROP TABLE IF EXISTS orders;",
            "DROP TABLE IF EXISTS users;",
            "DROP TABLE IF EXISTS employees_corp;",
            "DROP TABLE IF EXISTS departments_corp;",
            "DROP TABLE IF EXISTS subway_logs_linea_h;",
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
    {
        "id": 3,
        "title": "Análisis de Inventario: Productos Económicos",
        "coordinator_message_subject": "Directiva de Análisis de Mercado 003-C",
        "coordinator_message_body": "Analista, se requiere un listado de productos cuyo precio sea inferior a $50.00 para una campaña promocional. Por favor, extraiga el nombre, precio y stock de dichos productos.",
        "setup_sql": [
            "DROP TABLE IF EXISTS employees;",
            "DROP TABLE IF EXISTS documents;",
            "DROP TABLE IF EXISTS document_access_logs;",
            "DROP TABLE IF EXISTS products;",
            "DROP TABLE IF EXISTS orders;",
            "DROP TABLE IF EXISTS users;",
            "DROP TABLE IF EXISTS employees_corp;",
            "DROP TABLE IF EXISTS departments_corp;",
            "DROP TABLE IF EXISTS subway_logs_linea_h;",
            "CREATE TABLE products (product_id INTEGER PRIMARY KEY, name TEXT, price REAL, stock INTEGER);",
            "INSERT INTO products (product_id, name, price, stock) VALUES (101, 'Teclado Básico', 25.99, 150);",
            "INSERT INTO products (product_id, name, price, stock) VALUES (102, 'Mouse Óptico', 15.50, 200);",
            "INSERT INTO products (product_id, name, price, stock) VALUES (103, 'Monitor 22 pulgadas', 199.99, 50);",
            "INSERT INTO products (product_id, name, price, stock) VALUES (104, 'Webcam HD', 45.00, 75);",
            "INSERT INTO products (product_id, name, price, stock) VALUES (105, 'Hub USB', 12.75, 120);",
            "INSERT INTO products (product_id, name, price, stock) VALUES (106, 'Silla Ergonómica', 120.00, 25);"
        ],
        "correct_query": "SELECT name, price, stock FROM products WHERE price < 50.00 ORDER BY product_id ASC;",
        "evaluation_options": {
            'order_matters': True,
            'column_order_matters': True,
            'check_column_names': True
        },
        "hint": "Consulte la tabla 'products'. Filtre por la columna 'price' para valores menores a 50. Ordene por 'product_id'.",
        "success_message": "Listado de productos económicos generado. Información remitida al departamento de marketing."
    },
    {
        "id": 4,
        "title": "Auditoría de Pedidos: Historial Antiguo",
        "coordinator_message_subject": "Revisión de Historial de Transacciones 004-H",
        "coordinator_message_body": "Analista, es necesario identificar todas las órdenes realizadas antes del 1 de enero de 2024. Obtenga el ID de la orden, ID de cliente y fecha del pedido.",
        "setup_sql": [
            "DROP TABLE IF EXISTS employees;",
            "DROP TABLE IF EXISTS documents;",
            "DROP TABLE IF EXISTS document_access_logs;",
            "DROP TABLE IF EXISTS products;",
            "DROP TABLE IF EXISTS orders;",
            "DROP TABLE IF EXISTS users;",
            "DROP TABLE IF EXISTS employees_corp;",
            "DROP TABLE IF EXISTS departments_corp;",
            "DROP TABLE IF EXISTS subway_logs_linea_h;",
            "CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, total_amount REAL);",
            "INSERT INTO orders (order_id, customer_id, order_date, total_amount) VALUES (1, 10, '2023-11-15', 150.75);",
            "INSERT INTO orders (order_id, customer_id, order_date, total_amount) VALUES (2, 12, '2023-12-20', 345.00);",
            "INSERT INTO orders (order_id, customer_id, order_date, total_amount) VALUES (3, 10, '2024-01-05', 99.99);",
            "INSERT INTO orders (order_id, customer_id, order_date, total_amount) VALUES (4, 15, '2024-02-10', 210.50);",
            "INSERT INTO orders (order_id, customer_id, order_date, total_amount) VALUES (5, 12, '2023-10-01', 75.20);"
        ],
        "correct_query": "SELECT order_id, customer_id, order_date FROM orders WHERE order_date < '2024-01-01' ORDER BY order_date ASC;",
        "evaluation_options": {
            'order_matters': True,
            'column_order_matters': True,
            'check_column_names': True
        },
        "hint": "Consulte la tabla 'orders'. Filtre por la columna 'order_date' usando el formato 'YYYY-MM-DD'. Ordene por fecha.",
        "success_message": "Auditoría de pedidos antiguos completada. Registros relevantes identificados."
    },
    {
        "id": 5,
        "title": "Investigación Subte Línea H",
        "coordinator_message_subject": "Alerta de Seguridad: Actividad Sospechosa Línea H",
        "coordinator_message_body": (
            "Se necesita encontrar los sospechosos de un posible atentado contra la autoridad reguladora de información médica.\n"
            "Se solicita consultar la base de datos de usuarios del subte línea H desde las 8 a las 9 horas del día 14 de junio de 2025."
        ),
        "setup_sql": [
            "DROP TABLE IF EXISTS employees;",
            "DROP TABLE IF EXISTS documents;",
            "DROP TABLE IF EXISTS document_access_logs;",
            "DROP TABLE IF EXISTS products;",
            "DROP TABLE IF EXISTS orders;",
            "DROP TABLE IF EXISTS users;",
            "DROP TABLE IF EXISTS employees_corp;",
            "DROP TABLE IF EXISTS departments_corp;",
            "DROP TABLE IF EXISTS subway_logs_linea_h;",
            "CREATE TABLE subway_logs_linea_h (log_id INTEGER PRIMARY KEY AUTOINCREMENT, card_id TEXT NOT NULL, entry_station TEXT NOT NULL, entry_timestamp TEXT NOT NULL, exit_station TEXT, exit_timestamp TEXT, passenger_details TEXT);",
            "INSERT INTO subway_logs_linea_h (card_id, entry_station, entry_timestamp, exit_station, exit_timestamp, passenger_details) VALUES ('SUBE001', 'Corrientes', '2025-06-14 07:30:00', 'Hospitales', '2025-06-14 07:55:00', 'Hombre con maletín, nervioso.');",
            "INSERT INTO subway_logs_linea_h (card_id, entry_station, entry_timestamp, exit_station, exit_timestamp, passenger_details) VALUES ('SUBE002', 'Once', '2025-06-14 08:05:00', 'Inclán', '2025-06-14 08:25:00', 'Mujer con sombrero grande, mirando constantemente a su alrededor.');",
            "INSERT INTO subway_logs_linea_h (card_id, entry_station, entry_timestamp, exit_station, exit_timestamp, passenger_details) VALUES ('SUBE003', 'Santa Fe', '2025-06-14 08:15:00', 'Caseros', '2025-06-14 08:40:00', 'Persona con capucha y gafas de sol.');",
            "INSERT INTO subway_logs_linea_h (card_id, entry_station, entry_timestamp, exit_station, exit_timestamp, passenger_details) VALUES ('SUBE004', 'Corrientes', '2025-06-14 08:30:00', 'Parque Patricios', '2025-06-14 08:55:00', 'Joven con mochila, parece apurado.');",
            "INSERT INTO subway_logs_linea_h (card_id, entry_station, entry_timestamp, exit_station, exit_timestamp, passenger_details) VALUES ('SUBE005', 'Humberto I', '2025-06-14 08:45:00', 'Corrientes', '2025-06-14 09:10:00', 'Pasajero regular, leyendo el diario.');",
            "INSERT INTO subway_logs_linea_h (card_id, entry_station, entry_timestamp, exit_station, exit_timestamp, passenger_details) VALUES ('SUBE006', 'Inclán', '2025-06-14 08:58:00', 'Facultad de Derecho', '2025-06-14 09:20:00', 'Estudiante con libros.');",
            "INSERT INTO subway_logs_linea_h (card_id, entry_station, entry_timestamp, exit_station, exit_timestamp, passenger_details) VALUES ('SUBE007', 'Caseros', '2025-06-14 09:15:00', 'Once', '2025-06-14 09:35:00', 'Turista con cámara.');",
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
    },
    {
        "id": 6,
        "title": "Segmentación de Usuarios: Ciudad Capital",
        "coordinator_message_subject": "Análisis Demográfico 005-D",
        "coordinator_message_body": "Analista, necesitamos un listado de todos los usuarios registrados que residen en 'Ciudad Capital'. Incluya ID de usuario, nombre y email.",
        "setup_sql": [
            "DROP TABLE IF EXISTS employees;",
            "DROP TABLE IF EXISTS documents;",
            "DROP TABLE IF EXISTS document_access_logs;",
            "DROP TABLE IF EXISTS products;",
            "DROP TABLE IF EXISTS orders;",
            "DROP TABLE IF EXISTS users;",
            "DROP TABLE IF EXISTS employees_corp;",
            "DROP TABLE IF EXISTS departments_corp;",
            "DROP TABLE IF EXISTS subway_logs_linea_h;",
            "CREATE TABLE users (user_id INTEGER PRIMARY KEY, name TEXT, email TEXT, city TEXT, registration_date TEXT);",
            "INSERT INTO users (user_id, name, email, city, registration_date) VALUES (201, 'Carlos Vega', 'cvega@email.com', 'Ciudad Capital', '2023-03-12');",
            "INSERT INTO users (user_id, name, email, city, registration_date) VALUES (202, 'Ana Torres', 'atorres@email.com', 'Villa Norte', '2023-05-21');",
            "INSERT INTO users (user_id, name, email, city, registration_date) VALUES (203, 'Luis Paz', 'lpaz@email.com', 'Ciudad Capital', '2023-07-02');",
            "INSERT INTO users (user_id, name, email, city, registration_date) VALUES (204, 'Sofia Gomez', 'sgomez@email.com', 'Puerto Sur', '2024-01-15');",
            "INSERT INTO users (user_id, name, email, city, registration_date) VALUES (205, 'Martin Rivas', 'mrivas@email.com', 'Ciudad Capital', '2024-02-28');"
        ],
        "correct_query": "SELECT user_id, name, email FROM users WHERE city = 'Ciudad Capital' ORDER BY user_id ASC;",
        "evaluation_options": {
            'order_matters': True,
            'column_order_matters': True,
            'check_column_names': True
        },
        "hint": "Consulte la tabla 'users'. Filtre por la columna 'city' igual a 'Ciudad Capital'. Ordene por 'user_id'.",
        "success_message": "Listado de usuarios de Ciudad Capital extraído."
    },
    {
        "id": 7,
        "title": "Estructura Organizacional: Departamento de Ventas",
        "coordinator_message_subject": "Informe de Personal 006-P",
        "coordinator_message_body": "Analista, genere un informe que liste todos los empleados pertenecientes al departamento de 'Ventas'. Muestre el nombre del empleado y el nombre del departamento.",
        "setup_sql": [
            "DROP TABLE IF EXISTS employees;",
            "DROP TABLE IF EXISTS documents;",
            "DROP TABLE IF EXISTS document_access_logs;",
            "DROP TABLE IF EXISTS products;",
            "DROP TABLE IF EXISTS orders;",
            "DROP TABLE IF EXISTS users;",
            "DROP TABLE IF EXISTS employees_corp;",
            "DROP TABLE IF EXISTS departments_corp;",
            "DROP TABLE IF EXISTS subway_logs_linea_h;",
            "CREATE TABLE departments_corp (department_id INTEGER PRIMARY KEY, name TEXT UNIQUE);",
            "INSERT INTO departments_corp (department_id, name) VALUES (1, 'Recursos Humanos');",
            "INSERT INTO departments_corp (department_id, name) VALUES (2, 'Ingeniería');",
            "INSERT INTO departments_corp (department_id, name) VALUES (3, 'Ventas');",
            "INSERT INTO departments_corp (department_id, name) VALUES (4, 'Marketing');",
            "CREATE TABLE employees_corp (employee_id INTEGER PRIMARY KEY, name TEXT, department_id INTEGER, FOREIGN KEY(department_id) REFERENCES departments_corp(department_id));",
            "INSERT INTO employees_corp (employee_id, name, department_id) VALUES (1, 'Elena Navarro', 3);",
            "INSERT INTO employees_corp (employee_id, name, department_id) VALUES (2, 'Pedro Morales', 2);",
            "INSERT INTO employees_corp (employee_id, name, department_id) VALUES (3, 'Laura Jimenez', 3);",
            "INSERT INTO employees_corp (employee_id, name, department_id) VALUES (4, 'Fernando Costa', 4);",
            "INSERT INTO employees_corp (employee_id, name, department_id) VALUES (5, 'Sofia Herrera', 2);",
            "INSERT INTO employees_corp (employee_id, name, department_id) VALUES (6, 'Ricardo Gomez', 3);"
        ],
        "correct_query": "SELECT ec.name, dc.name AS department_name FROM employees_corp ec JOIN departments_corp dc ON ec.department_id = dc.department_id WHERE dc.name = 'Ventas' ORDER BY ec.employee_id ASC;",
        "evaluation_options": {
            'order_matters': True,
            'column_order_matters': True,
            'check_column_names': True
        },
        "hint": "Use JOIN para combinar 'employees_corp' y 'departments_corp' por 'department_id'. Filtre donde el nombre del departamento sea 'Ventas'. Ordene por 'employee_id'.",
        "success_message": "Informe de empleados del departamento de Ventas generado."
    }
]
