# Secuelas/config.py

# Poner en True para forzar recarga completa de misiones desde este archivo
# (borra y re-inserta todas las misiones en la BD al iniciar la app)
FORCE_RELOAD_MISSIONS = True

# ─── Drops de todas las tablas posibles ──────────────────────────────────────
_DROPS = [
    # Tablas nuevas (20 misiones)
    "DROP TABLE IF EXISTS empleados;",
    "DROP TABLE IF EXISTS departamentos;",
    "DROP TABLE IF EXISTS empleados_dept;",
    "DROP TABLE IF EXISTS documentos;",
    "DROP TABLE IF EXISTS registros_acceso;",
    "DROP TABLE IF EXISTS registros_metro;",
    "DROP TABLE IF EXISTS inventario;",
    "DROP TABLE IF EXISTS transacciones;",
    "DROP TABLE IF EXISTS proveedores;",
    "DROP TABLE IF EXISTS contratos;",
    "DROP TABLE IF EXISTS ordenes_vigilancia;",
    "DROP TABLE IF EXISTS evidencias;",
    # Tablas de la versión anterior (compatibilidad)
    "DROP TABLE IF EXISTS employees;",
    "DROP TABLE IF EXISTS documents;",
    "DROP TABLE IF EXISTS document_access_logs;",
    "DROP TABLE IF EXISTS products;",
    "DROP TABLE IF EXISTS orders;",
    "DROP TABLE IF EXISTS users;",
    "DROP TABLE IF EXISTS employees_corp;",
    "DROP TABLE IF EXISTS departments_corp;",
    "DROP TABLE IF EXISTS subway_logs_linea_h;",
    "DROP TABLE IF EXISTS access_logs;",
    "DROP TABLE IF EXISTS classified_documents;",
    "DROP TABLE IF EXISTS surveillance_orders;",
    "DROP TABLE IF EXISTS evidence_log;",
]

# ─── Bloques de datos reutilizables ──────────────────────────────────────────

_CREATE_EMPLEADOS = (
    "CREATE TABLE empleados (id INTEGER PRIMARY KEY, nombre TEXT, "
    "departamento TEXT, cargo TEXT, nivel_acceso INTEGER, "
    "fecha_ingreso TEXT, tarjeta_metro TEXT);"
)
_INSERT_EMPLEADOS = [
    "INSERT INTO empleados VALUES (1, 'Analista 734 (Usted)', 'Análisis de Datos', 'Analista Jr.', 2, '2025-05-12', 'SUBE-734');",
    "INSERT INTO empleados VALUES (2, 'Coordinadora Vera', 'Análisis de Datos', 'Coordinadora', 3, '2022-03-08', 'SUBE-VER');",
    "INSERT INTO empleados VALUES (3, 'Agente Nova K', 'Consultoría Externa', 'Especialista en Seguridad', 4, '2024-11-15', 'SUBE-NOV');",
    "INSERT INTO empleados VALUES (4, 'Director Kael Umbra', 'Alta Dirección', 'Director General', 5, '2010-01-20', 'SUBE-KAE');",
    "INSERT INTO empleados VALUES (5, 'Archivista Rho', 'Archivo y Documentación', 'Archivista Principal', 2, '2017-09-03', 'SUBE-RHO');",
    "INSERT INTO empleados VALUES (6, 'Supervisor Maren', 'Análisis de Datos', 'Supervisor Senior', 3, '2020-06-15', 'SUBE-MAR');",
    "INSERT INTO empleados VALUES (7, 'Técnico Solt', 'Infraestructura', 'Técnico de Sistemas', 2, '2021-11-28', 'SUBE-SOL');",
]

_CREATE_REGISTROS_ACCESO = (
    "CREATE TABLE registros_acceso (id INTEGER PRIMARY KEY, empleado_id INTEGER, "
    "empleado_nombre TEXT, documento_id INTEGER, clasificacion TEXT, fecha TEXT);"
)
_INSERT_REGISTROS_ACCESO = [
    "INSERT INTO registros_acceso VALUES (1, 3, 'Agente Nova K', 2, 'SECRETO', '2025-06-09');",
    "INSERT INTO registros_acceso VALUES (2, 3, 'Agente Nova K', 3, 'SECRETO', '2025-06-10');",
    "INSERT INTO registros_acceso VALUES (3, 4, 'Director Kael Umbra', 2, 'SECRETO', '2025-06-10');",
    "INSERT INTO registros_acceso VALUES (4, 4, 'Director Kael Umbra', 3, 'SECRETO', '2025-06-11');",
    "INSERT INTO registros_acceso VALUES (5, 4, 'Director Kael Umbra', 7, 'SECRETO', '2025-06-12');",
    "INSERT INTO registros_acceso VALUES (6, 4, 'Director Kael Umbra', 2, 'SECRETO', '2025-06-13');",
    "INSERT INTO registros_acceso VALUES (7, 4, 'Director Kael Umbra', 7, 'SECRETO', '2025-06-13');",
    "INSERT INTO registros_acceso VALUES (8, 4, 'Director Kael Umbra', 2, 'SECRETO', '2025-06-14');",
    "INSERT INTO registros_acceso VALUES (9, 1, 'Analista 734 (Usted)', 1, 'PÚBLICO', '2025-06-14');",
    "INSERT INTO registros_acceso VALUES (10, 5, 'Archivista Rho', 4, 'RESERVADO', '2025-06-08');",
    "INSERT INTO registros_acceso VALUES (11, 5, 'Archivista Rho', 8, 'RESERVADO', '2025-06-09');",
    "INSERT INTO registros_acceso VALUES (12, 2, 'Coordinadora Vera', 2, 'SECRETO', '2025-06-14');",
    "INSERT INTO registros_acceso VALUES (13, 3, 'Agente Nova K', 2, 'SECRETO', '2025-06-11');",
    "INSERT INTO registros_acceso VALUES (14, 3, 'Agente Nova K', 7, 'SECRETO', '2025-06-12');",
    "INSERT INTO registros_acceso VALUES (15, 2, 'Coordinadora Vera', 3, 'SECRETO', '2025-06-10');",
    "INSERT INTO registros_acceso VALUES (16, 2, 'Coordinadora Vera', 7, 'SECRETO', '2025-06-11');",
]

_CREATE_REGISTROS_METRO = (
    "CREATE TABLE registros_metro (id INTEGER PRIMARY KEY, tarjeta_id TEXT, "
    "estacion_entrada TEXT, timestamp_entrada TEXT, estacion_salida TEXT, "
    "timestamp_salida TEXT, fecha TEXT);"
)
_INSERT_REGISTROS_METRO = [
    "INSERT INTO registros_metro VALUES (1, 'SUBE-NOV', 'Plaza Central', '2025-06-14 07:45:00', 'Archivo Nacional', '2025-06-14 08:10:00', '2025-06-14');",
    "INSERT INTO registros_metro VALUES (2, 'SUBE-KAE', 'Ministerio', '2025-06-14 08:00:00', NULL, NULL, '2025-06-14');",
    "INSERT INTO registros_metro VALUES (3, 'SUBE-734', 'Plaza Central', '2025-06-14 08:30:00', 'Plaza Central', '2025-06-14 09:00:00', '2025-06-14');",
    "INSERT INTO registros_metro VALUES (4, 'SUBE-RHO', 'Archivo Nacional', '2025-06-14 07:30:00', 'Plaza Central', '2025-06-14 08:00:00', '2025-06-14');",
    "INSERT INTO registros_metro VALUES (5, 'SUBE-KAE', 'Archivo Nacional', '2025-06-13 22:00:00', NULL, NULL, '2025-06-13');",
    "INSERT INTO registros_metro VALUES (6, 'SUBE-EXT1', 'Ministerio', '2025-06-14 07:55:00', NULL, NULL, '2025-06-14');",
    "INSERT INTO registros_metro VALUES (7, 'SUBE-MAR', 'Plaza Central', '2025-06-14 09:15:00', 'Ministerio', '2025-06-14 09:45:00', '2025-06-14');",
    "INSERT INTO registros_metro VALUES (8, 'SUBE-EXT2', 'Archivo Nacional', '2025-06-14 21:30:00', NULL, NULL, '2025-06-14');",
    "INSERT INTO registros_metro VALUES (9, 'SUBE-RHO', 'Ministerio', '2025-06-13 20:00:00', 'Archivo Nacional', '2025-06-13 21:00:00', '2025-06-13');",
    "INSERT INTO registros_metro VALUES (10, 'SUBE-VER', 'Ministerio', '2025-06-14 08:15:00', 'Plaza Central', '2025-06-14 08:50:00', '2025-06-14');",
    "INSERT INTO registros_metro VALUES (11, 'SUBE-SOL', 'Terminal Sur', '2025-06-14 07:00:00', 'Residencial Norte', '2025-06-14 07:30:00', '2025-06-14');",
]

# ─── Lista de Misiones ────────────────────────────────────────────────────────
MISSIONS = [

    # ══════════════════════════════════════════════════════════════════════════
    # ACTO I — EL SISTEMA (Misiones 1–7)
    # Conceptos: SELECT, WHERE, LIKE, IN, ORDER BY, LIMIT
    # ══════════════════════════════════════════════════════════════════════════

    {
        "id": 1,
        "title": "Primer Día en la UEI",
        "coordinator_message_subject": "Directiva de Incorporación — Analista 734",
        "coordinator_message_body": (
            "Analista 734, bienvenido a la Unidad de Escrutinio Informativo.\n\n"
            "Soy la Coordinadora Vera, responsable del equipo de Análisis de Datos.\n"
            "Antes de asignarle su primera directiva operacional, necesitamos que se "
            "familiarice con el personal de la Unidad.\n\n"
            "Acceda a la tabla 'empleados' y presente el listado completo del equipo, "
            "ordenado por ID de forma ascendente.\n\n"
            "— Coordinadora Vera, Análisis de Datos"
        ),
        "setup_sql": _DROPS + [
            _CREATE_EMPLEADOS,
        ] + _INSERT_EMPLEADOS,
        "correct_query": (
            "SELECT * FROM empleados ORDER BY id ASC;"
        ),
        "evaluation_options": {
            "order_matters": True,
            "column_order_matters": True,
            "check_column_names": True
        },
        "hint": "Consulta la tabla principal de personal del sistema sin filtros. | Use SELECT * FROM empleados para obtener todas las columnas. Agregue ORDER BY id ASC.",
        "success_message": (
            "Incorporación registrada. Su expediente ha sido creado en el sistema.\n\n"
            "Somos siete en total. Guarde bien estos nombres — los necesitará."
        )
    },

    {
        "id": 2,
        "title": "Directorio Oficial",
        "coordinator_message_subject": "Solicitud: Directorio de Personal — Portal Interno",
        "coordinator_message_body": (
            "Analista 734.\n\n"
            "El portal interno necesita actualizar el directorio de personal visible "
            "para todas las dependencias.\n\n"
            "Genere un listado con solo tres columnas: nombre, cargo y departamento "
            "de cada empleado. Ordene alfabéticamente por nombre.\n\n"
            "No incluya información sensible como nivel de acceso o fecha de ingreso.\n\n"
            "— Coordinadora Vera"
        ),
        "setup_sql": _DROPS + [
            _CREATE_EMPLEADOS,
        ] + _INSERT_EMPLEADOS,
        "correct_query": (
            "SELECT nombre, cargo, departamento FROM empleados ORDER BY nombre ASC;"
        ),
        "evaluation_options": {
            "order_matters": True,
            "column_order_matters": True,
            "check_column_names": True
        },
        "hint": "No todas las columnas son necesarias, elige solo las solicitadas. | Especifique las columnas nombre, cargo, departamento en el SELECT. Use ORDER BY nombre ASC.",
        "success_message": (
            "Directorio generado y publicado en el portal interno.\n\n"
            "Nota personal: el Agente Nova K figura como 'Consultoría Externa'. "
            "Los contratistas externos con nivel de acceso 4 son inusuales."
        )
    },

    {
        "id": 3,
        "title": "Auditoría de Personal Interno",
        "coordinator_message_subject": "URGENTE — Separación de Registros: Personal Interno vs. Externo",
        "coordinator_message_body": (
            "Analista 734.\n\n"
            "El Departamento de Control solicitó una separación inmediata de registros. "
            "Por razones de protocolo, los consultores externos deben quedar excluidos "
            "de los informes de personal de plantilla.\n\n"
            "Extraiga id, nombre, cargo y nivel_acceso de todos los empleados "
            "cuyo departamento NO sea 'Consultoría Externa'.\n"
            "Ordene por nivel_acceso descendente; en caso de empate, por nombre ascendente.\n\n"
            "— Coordinadora Vera"
        ),
        "setup_sql": _DROPS + [
            _CREATE_EMPLEADOS,
        ] + _INSERT_EMPLEADOS,
        "correct_query": (
            "SELECT id, nombre, cargo, nivel_acceso "
            "FROM empleados "
            "WHERE departamento != 'Consultoría Externa' "
            "ORDER BY nivel_acceso DESC, nombre ASC;"
        ),
        "evaluation_options": {
            "order_matters": True,
            "column_order_matters": True,
            "check_column_names": True
        },
        "hint": "Hay un departamento que no deberia aparecer en los resultados. | Use WHERE departamento != para excluir. Ordene con ORDER BY nivel_acceso DESC, nombre ASC.",
        "success_message": (
            "Lista de personal interno extraída. Seis empleados en plantilla.\n\n"
            "La brecha de nivel_acceso entre el Director Umbra (5) y el resto del equipo (2-3) "
            "es llamativa. Un solo hombre concentra el acceso máximo."
        )
    },

    {
        "id": 4,
        "title": "Personal de Alto Clearance",
        "coordinator_message_subject": "Convocatoria Clasificada — Sesión Informativa Nivel 4+",
        "coordinator_message_body": (
            "Analista 734.\n\n"
            "Se convoca una sesión informativa de carácter clasificado. "
            "Por directiva de seguridad, solo pueden asistir empleados con "
            "nivel de acceso 4 o 5.\n\n"
            "Genere la lista de convocados: nombre, cargo y nivel_acceso. "
            "Filtre usando BETWEEN para el rango de niveles permitidos. "
            "Ordene por nivel_acceso descendente y, en caso de empate, por nombre ascendente.\n\n"
            "— Coordinadora Vera"
        ),
        "setup_sql": _DROPS + [
            _CREATE_EMPLEADOS,
        ] + _INSERT_EMPLEADOS,
        "correct_query": (
            "SELECT nombre, cargo, nivel_acceso "
            "FROM empleados "
            "WHERE nivel_acceso BETWEEN 4 AND 5 "
            "ORDER BY nivel_acceso DESC, nombre ASC;"
        ),
        "evaluation_options": {
            "order_matters": True,
            "column_order_matters": True,
            "check_column_names": True
        },
        "hint": "El nivel de acceso tiene un rango acotado, busca un operador para rangos. | Use WHERE nivel_acceso BETWEEN 4 AND 5. Ordene con ORDER BY nivel_acceso DESC, nombre ASC.",
        "success_message": (
            "Convocatoria enviada a 2 personas.\n\n"
            "Observación: el Agente Nova K, contratista externo, tiene nivel de acceso 4 — "
            "el mismo que personal de dirección interna. "
            "¿Quién autorizó ese nivel de clearance para un consultor externo?"
        )
    },

    {
        "id": 5,
        "title": "Búsqueda de Documentos Sensibles",
        "coordinator_message_subject": "CIFRADO — Hay documentos que no deberían existir",
        "coordinator_message_body": (
            "Analista 734. Aquí Archivista Rho — canal no oficial.\n\n"
            "Llevo semanas revisando el inventario de documentos clasificados "
            "y encontré algo que me preocupa.\n\n"
            "Empiece por lo más visible: busque en la tabla 'documentos' todos "
            "los registros cuyo título contenga la palabra 'Protocolo'.\n"
            "Muestre: id, titulo, clasificacion, fecha_creacion.\n"
            "Ordene por fecha_creacion ascendente.\n\n"
            "No comente esto con nadie en la Unidad todavía.\n\n"
            "— Rho [canal lateral]"
        ),
        "setup_sql": _DROPS + [
            "CREATE TABLE documentos (id INTEGER PRIMARY KEY, titulo TEXT, "
            "clasificacion TEXT, fecha_creacion TEXT);",
            "INSERT INTO documentos VALUES (1, 'Manual de Incorporación UEI', 'PÚBLICO', '2025-01-01');",
            "INSERT INTO documentos VALUES (2, 'Protocolo Omega-7', 'SECRETO', '2024-03-15');",
            "INSERT INTO documentos VALUES (3, 'Protocolo de Vigilancia Ciudadana', 'SECRETO', '2024-06-20');",
            "INSERT INTO documentos VALUES (4, 'Informe Anual 2024', 'RESERVADO', '2024-12-31');",
            "INSERT INTO documentos VALUES (5, 'Expediente: Analista 734', 'ULTRA-SECRETO', '2025-05-12');",
            "INSERT INTO documentos VALUES (6, 'Operación SECUELAS', 'ULTRA-SECRETO', '2025-01-01');",
            "INSERT INTO documentos VALUES (7, 'Protocolo de Emergencia', 'SECRETO', '2025-02-14');",
            "INSERT INTO documentos VALUES (8, 'Directivas de Campo 2025', 'RESERVADO', '2025-03-01');",
        ],
        "correct_query": (
            "SELECT id, titulo, clasificacion, fecha_creacion "
            "FROM documentos "
            "WHERE titulo LIKE '%Protocolo%' "
            "ORDER BY fecha_creacion ASC;"
        ),
        "evaluation_options": {
            "order_matters": True,
            "column_order_matters": True,
            "check_column_names": True
        },
        "hint": "Un titulo de documento contiene una palabra clave especifica. | Use WHERE titulo LIKE con el signo % antes y despues de la palabra buscada.",
        "success_message": (
            "Tres protocolos hallados, todos clasificados como SECRETO.\n\n"
            "El más antiguo: 'Protocolo de Vigilancia Ciudadana', creado en junio de 2024. "
            "Lleva más de un año en el sistema. ¿Quién lo autorizó? "
            "No figura en ningún registro de aprobación que yo haya visto."
        )
    },

    {
        "id": 6,
        "title": "Movimientos en Zonas Sensibles",
        "coordinator_message_subject": "Alerta — Análisis de Movilidad: Incidente 14-Jun-2025",
        "coordinator_message_body": (
            "Analista 734.\n\n"
            "El 14 de junio de 2025 hubo un incidente de seguridad no documentado. "
            "Como parte de la investigación, necesitamos rastrear los movimientos del "
            "sistema de metro en las zonas de interés ese día.\n\n"
            "Consulte la tabla 'registros_metro'. Filtre todos los registros donde "
            "la estacion_entrada sea alguna de estas tres: "
            "'Plaza Central', 'Ministerio' o 'Archivo Nacional'.\n"
            "Muestre: id, tarjeta_id, estacion_entrada, timestamp_entrada.\n"
            "Ordene por timestamp_entrada ascendente.\n\n"
            "— Coordinadora Vera"
        ),
        "setup_sql": _DROPS + [
            _CREATE_REGISTROS_METRO,
        ] + _INSERT_REGISTROS_METRO,
        "correct_query": (
            "SELECT id, tarjeta_id, estacion_entrada, timestamp_entrada "
            "FROM registros_metro "
            "WHERE estacion_entrada IN ('Plaza Central', 'Ministerio', 'Archivo Nacional') "
            "ORDER BY timestamp_entrada ASC;"
        ),
        "evaluation_options": {
            "order_matters": True,
            "column_order_matters": True,
            "check_column_names": True
        },
        "hint": "Los registros de acceso fisico revelan por que estaciones paso alguien. | Use WHERE estacion_entrada IN con las tres zonas de interes. Luego ORDER BY timestamp_entrada ASC.",
        "success_message": (
            "10 movimientos detectados en zonas de interés.\n\n"
            "Hay dos tarjetas no identificadas: SUBE-EXT1 (ingresó al Ministerio a las 07:55) "
            "y SUBE-EXT2 (ingresó al Archivo Nacional a las 21:30). "
            "Esas tarjetas no figuran en ningún registro de la UEI."
        )
    },

    {
        "id": 7,
        "title": "Los Últimos Registros",
        "coordinator_message_subject": "URGENTE — Top 4 Entradas Recientes: 14-Jun-2025",
        "coordinator_message_body": (
            "Analista 734.\n\n"
            "Tiempo de respuesta crítico. El equipo de seguridad necesita los cuatro "
            "últimos registros de entrada al sistema de metro correspondientes al "
            "14 de junio de 2025.\n\n"
            "De la tabla 'registros_metro', filtre por fecha '2025-06-14'.\n"
            "Muestre tarjeta_id, estacion_entrada y timestamp_entrada.\n"
            "Ordene por timestamp_entrada descendente y limite a 4 resultados.\n\n"
            "— Coordinadora Vera"
        ),
        "setup_sql": _DROPS + [
            _CREATE_REGISTROS_METRO,
        ] + _INSERT_REGISTROS_METRO,
        "correct_query": (
            "SELECT tarjeta_id, estacion_entrada, timestamp_entrada "
            "FROM registros_metro "
            "WHERE fecha = '2025-06-14' "
            "ORDER BY timestamp_entrada DESC "
            "LIMIT 4;"
        ),
        "evaluation_options": {
            "order_matters": True,
            "column_order_matters": True,
            "check_column_names": True
        },
        "hint": "Necesitas filtrar por una fecha especifica y limitar cuantos resultados ves. | Filtre con WHERE fecha = la fecha buscada, ordene DESC y use LIMIT 4 al final.",
        "success_message": (
            "El último registro del día es SUBE-EXT2 en el Archivo Nacional a las 21:30.\n\n"
            "Una tarjeta no identificada en un archivo clasificado, de noche. "
            "El sistema de metro no registra su salida. "
            "Alguien entró al archivo y no salió por los canales habituales."
        )
    },

    # ══════════════════════════════════════════════════════════════════════════
    # ACTO II — CONEXIONES (Misiones 8–11)
    # Conceptos: INNER JOIN, LEFT JOIN, IS NULL, expresiones aritméticas
    # ══════════════════════════════════════════════════════════════════════════

    {
        "id": 8,
        "title": "Estructura y Presupuesto",
        "coordinator_message_subject": "Solicitud Finanzas — Cruce Empleados/Presupuesto Departamental",
        "coordinator_message_body": (
            "Analista 734.\n\n"
            "El área de Finanzas solicita un informe cruzado: necesitan saber el "
            "presupuesto asignado al departamento de cada empleado.\n\n"
            "Tiene dos tablas disponibles:\n"
            "  'empleados_dept' — con id, nombre, departamento_id, cargo\n"
            "  'departamentos'  — con id, nombre, presupuesto\n\n"
            "Una ambas tablas. Muestre el nombre del empleado, el nombre del departamento "
            "y el presupuesto. Ordene por presupuesto descendente; en empates, por nombre "
            "del empleado ascendente.\n\n"
            "— Coordinadora Vera"
        ),
        "setup_sql": _DROPS + [
            "CREATE TABLE departamentos (id INTEGER PRIMARY KEY, nombre TEXT, presupuesto INTEGER);",
            "INSERT INTO departamentos VALUES (1, 'Análisis de Datos', 50000);",
            "INSERT INTO departamentos VALUES (2, 'Alta Dirección', 200000);",
            "INSERT INTO departamentos VALUES (3, 'Consultoría Externa', 0);",
            "INSERT INTO departamentos VALUES (4, 'Infraestructura', 30000);",
            "INSERT INTO departamentos VALUES (5, 'Archivo y Documentación', 15000);",
            "CREATE TABLE empleados_dept (id INTEGER PRIMARY KEY, nombre TEXT, departamento_id INTEGER, cargo TEXT);",
            "INSERT INTO empleados_dept VALUES (1, 'Analista 734 (Usted)', 1, 'Analista Jr.');",
            "INSERT INTO empleados_dept VALUES (2, 'Coordinadora Vera', 1, 'Coordinadora');",
            "INSERT INTO empleados_dept VALUES (3, 'Agente Nova K', 3, 'Especialista en Seguridad');",
            "INSERT INTO empleados_dept VALUES (4, 'Director Kael Umbra', 2, 'Director General');",
            "INSERT INTO empleados_dept VALUES (5, 'Archivista Rho', 5, 'Archivista Principal');",
            "INSERT INTO empleados_dept VALUES (6, 'Supervisor Maren', 1, 'Supervisor Senior');",
            "INSERT INTO empleados_dept VALUES (7, 'Técnico Solt', 4, 'Técnico de Sistemas');",
        ],
        "correct_query": (
            "SELECT e.nombre, d.nombre AS departamento, d.presupuesto "
            "FROM empleados_dept e "
            "JOIN departamentos d ON e.departamento_id = d.id "
            "ORDER BY d.presupuesto DESC, e.nombre ASC;"
        ),
        "evaluation_options": {
            "order_matters": True,
            "column_order_matters": True,
            "check_column_names": True
        },
        "hint": "La informacion que necesitas esta en dos tablas, debes combinarlas. | Use JOIN departamentos ON e.departamento_id = d.id. Alias el nombre del departamento. Ordene por presupuesto DESC.",
        "success_message": (
            "Informe de presupuesto generado.\n\n"
            "Alta Dirección tiene 200.000 créditos — cuatro veces más que Análisis de Datos. "
            "Un único empleado administra ese presupuesto: el Director Kael Umbra. "
            "Y el departamento de Consultoría Externa, donde figura Nova K, tiene asignado 0 créditos. "
            "¿Cómo se financian sus honorarios?"
        )
    },

    {
        "id": 9,
        "title": "Archivos Sin Rastro",
        "coordinator_message_subject": "CIFRADO NIV.3 — Documentos Consultados Sin Registro",
        "coordinator_message_body": (
            "Analista 734. Rho de nuevo — canal cifrado.\n\n"
            "Encontré algo grave. Hay documentos en el inventario oficial que "
            "nunca aparecen en los registros de acceso. Eso no debería ser posible: "
            "cualquier consulta a un documento clasificado genera un log automático.\n\n"
            "A menos que alguien los haya leído evadiendo el sistema de auditoría.\n\n"
            "Haga un LEFT JOIN entre 'documentos' (alias d) y 'registros_acceso' (alias ra) "
            "usando d.id = ra.documento_id. Filtre donde ra.id IS NULL.\n"
            "Muestre: d.id, d.titulo, d.clasificacion.\n"
            "Ordene por d.id ascendente.\n\n"
            "— Rho [CANAL CIFRADO]"
        ),
        "setup_sql": _DROPS + [
            "CREATE TABLE documentos (id INTEGER PRIMARY KEY, titulo TEXT, "
            "clasificacion TEXT, fecha_creacion TEXT);",
            "INSERT INTO documentos VALUES (1, 'Manual de Incorporación UEI', 'PÚBLICO', '2025-01-01');",
            "INSERT INTO documentos VALUES (2, 'Protocolo Omega-7', 'SECRETO', '2024-03-15');",
            "INSERT INTO documentos VALUES (3, 'Protocolo de Vigilancia Ciudadana', 'SECRETO', '2024-06-20');",
            "INSERT INTO documentos VALUES (4, 'Informe Anual 2024', 'RESERVADO', '2024-12-31');",
            "INSERT INTO documentos VALUES (5, 'Expediente: Analista 734', 'ULTRA-SECRETO', '2025-05-12');",
            "INSERT INTO documentos VALUES (6, 'Operación SECUELAS', 'ULTRA-SECRETO', '2025-01-01');",
            "INSERT INTO documentos VALUES (7, 'Protocolo de Emergencia', 'SECRETO', '2025-02-14');",
            "INSERT INTO documentos VALUES (8, 'Directivas de Campo 2025', 'RESERVADO', '2025-03-01');",
            _CREATE_REGISTROS_ACCESO,
        ] + _INSERT_REGISTROS_ACCESO,
        "correct_query": (
            "SELECT d.id, d.titulo, d.clasificacion "
            "FROM documentos d "
            "LEFT JOIN registros_acceso ra ON d.id = ra.documento_id "
            "WHERE ra.id IS NULL "
            "ORDER BY d.id ASC;"
        ),
        "evaluation_options": {
            "order_matters": True,
            "column_order_matters": True,
            "check_column_names": True
        },
        "hint": "Busca documentos que no tienen ningun registro asociado en otra tabla. | Use LEFT JOIN registros_acceso ON d.id = ra.documento_id. Luego filtre WHERE ra.id IS NULL.",
        "success_message": (
            "Dos documentos ULTRA-SECRETO sin ningún registro de acceso oficial:\n\n"
            "  · Expediente: Analista 734 — creado el 12 de mayo de 2025\n"
            "  · Operación SECUELAS — creado el 1 de enero de 2025\n\n"
            "Fueron creados pero nunca leídos... oficialmente. "
            "El expediente fue creado dos días antes de que usted se incorporara a la UEI."
        )
    },

    {
        "id": 10,
        "title": "Pasajeros que Desaparecieron",
        "coordinator_message_subject": "Error Crítico — Registros de Salida Faltantes: 14-Jun-2025",
        "coordinator_message_body": (
            "Analista 734.\n\n"
            "El sistema de control del metro reportó una anomalía: varios pasajeros "
            "del 14 de junio tienen registro de entrada pero no de salida.\n\n"
            "Identifique las tarjetas con timestamp_salida nulo en esa fecha. "
            "De la tabla 'registros_metro', filtre por fecha '2025-06-14' "
            "y donde timestamp_salida IS NULL.\n"
            "Muestre: tarjeta_id, estacion_entrada, timestamp_entrada.\n"
            "Ordene por timestamp_entrada ascendente.\n\n"
            "— Coordinadora Vera"
        ),
        "setup_sql": _DROPS + [
            _CREATE_REGISTROS_METRO,
        ] + _INSERT_REGISTROS_METRO,
        "correct_query": (
            "SELECT tarjeta_id, estacion_entrada, timestamp_entrada "
            "FROM registros_metro "
            "WHERE fecha = '2025-06-14' "
            "AND timestamp_salida IS NULL "
            "ORDER BY timestamp_entrada ASC;"
        ),
        "evaluation_options": {
            "order_matters": True,
            "column_order_matters": True,
            "check_column_names": True
        },
        "hint": "Hay viajes sin registro de salida, busca campos vacios en esa columna. | Use WHERE fecha = la fecha buscada AND timestamp_salida IS NULL. IS NULL detecta campos vacios.",
        "success_message": (
            "Tres entradas sin salida registrada:\n\n"
            "  · SUBE-EXT1 — Ministerio, 07:55\n"
            "  · SUBE-KAE  — Ministerio, 08:00\n"
            "  · SUBE-EXT2 — Archivo Nacional, 21:30\n\n"
            "SUBE-KAE pertenece al Director Kael Umbra. "
            "Entró al Ministerio a las 8 de la mañana y no hay registro de que haya salido."
        )
    },

    {
        "id": 11,
        "title": "Irregularidades en el Inventario",
        "coordinator_message_subject": "Auditoría de Inventario — Cálculo de Valor Total por Ítem",
        "coordinator_message_body": (
            "Analista 734.\n\n"
            "La Contraloría interna detectó posibles irregularidades en las adquisiciones "
            "de equipamiento. Necesitamos calcular el valor total de cada ítem "
            "(precio_unitario × cantidad) y focalizar en los de mayor impacto.\n\n"
            "De la tabla 'inventario', calcule el valor total como columna 'valor_total'. "
            "Muestre: nombre, precio_unitario, cantidad, valor_total.\n"
            "Filtre solo los ítems cuyo valor total supere los 10.000 créditos.\n"
            "Ordene por valor_total descendente.\n\n"
            "— Coordinadora Vera"
        ),
        "setup_sql": _DROPS + [
            "CREATE TABLE inventario (id INTEGER PRIMARY KEY, nombre TEXT, "
            "precio_unitario REAL, cantidad INTEGER, departamento TEXT);",
            "INSERT INTO inventario VALUES (1, 'Servidor Rack A', 8500.00, 3, 'Alta Dirección');",
            "INSERT INTO inventario VALUES (2, 'Monitor 4K', 350.00, 20, 'Análisis de Datos');",
            "INSERT INTO inventario VALUES (3, 'Estación de Trabajo Segura', 2200.00, 8, 'Análisis de Datos');",
            "INSERT INTO inventario VALUES (4, 'Equipo de Cifrado', 15000.00, 5, 'Alta Dirección');",
            "INSERT INTO inventario VALUES (5, 'Silla Ergonómica', 180.00, 50, 'Infraestructura');",
            "INSERT INTO inventario VALUES (6, 'Software de Vigilancia Pro', 45000.00, 2, 'Alta Dirección');",
            "INSERT INTO inventario VALUES (7, 'Cable de Red', 12.00, 500, 'Infraestructura');",
            "INSERT INTO inventario VALUES (8, 'Tablet de Campo', 800.00, 10, 'Consultoría Externa');",
        ],
        "correct_query": (
            "SELECT nombre, precio_unitario, cantidad, precio_unitario * cantidad AS valor_total "
            "FROM inventario "
            "WHERE precio_unitario * cantidad > 10000 "
            "ORDER BY valor_total DESC;"
        ),
        "evaluation_options": {
            "order_matters": True,
            "column_order_matters": True,
            "check_column_names": True
        },
        "hint": "El valor total de cada item se calcula multiplicando dos columnas. | Calcule precio_unitario * cantidad AS valor_total. Use esa misma expresion en WHERE para filtrar.",
        "success_message": (
            "Cuatro ítems superan los 10.000 créditos. Total: 208.100 créditos.\n\n"
            "El Software de Vigilancia Pro (90.000) y el Equipo de Cifrado (75.000) "
            "corresponden ambos al departamento de Alta Dirección. "
            "El presupuesto anual de ese departamento es 200.000 créditos. "
            "Solo en dos ítems ya comprometieron el 82% del presupuesto."
        )
    },

    # ══════════════════════════════════════════════════════════════════════════
    # ACTO III — EL PATRÓN (Misiones 12–14)
    # Conceptos: GROUP BY, COUNT/SUM/MAX, HAVING
    # ══════════════════════════════════════════════════════════════════════════

    {
        "id": 12,
        "title": "El Patrón de Accesos",
        "coordinator_message_subject": "CIFRADO — Los Números No Mienten",
        "coordinator_message_body": (
            "Analista 734. Rho.\n\n"
            "Ejecute esto ahora. No me pregunte cómo obtuve acceso a este canal.\n\n"
            "En la tabla 'registros_acceso', cuente cuántos accesos a documentos "
            "SECRETO tuvo cada empleado (columna empleado_nombre).\n"
            "Muestre: empleado_nombre y el conteo como 'total_accesos'.\n"
            "Filtre solo clasificacion = 'SECRETO'.\n"
            "Ordene por total_accesos descendente; en empate, por empleado_nombre ascendente.\n\n"
            "Los números no mienten.\n\n"
            "— Rho"
        ),
        "setup_sql": _DROPS + [
            _CREATE_REGISTROS_ACCESO,
        ] + _INSERT_REGISTROS_ACCESO,
        "correct_query": (
            "SELECT empleado_nombre, COUNT(*) AS total_accesos "
            "FROM registros_acceso "
            "WHERE clasificacion = 'SECRETO' "
            "GROUP BY empleado_nombre "
            "ORDER BY total_accesos DESC, empleado_nombre ASC;"
        ),
        "evaluation_options": {
            "order_matters": True,
            "column_order_matters": True,
            "check_column_names": True
        },
        "hint": "Necesitas contar cuantas veces aparece cada nombre en cierta categoria. | Use GROUP BY empleado_nombre y COUNT(*) AS total_accesos. Filtre con WHERE clasificacion primero.",
        "success_message": (
            "Tres personas accedieron a documentos SECRETO esta semana:\n\n"
            "  · Director Kael Umbra  — 6 accesos\n"
            "  · Agente Nova K        — 4 accesos\n"
            "  · Coordinadora Vera    — 3 accesos\n\n"
            "El Director General encabeza la lista por un margen amplio. "
            "Los tres comparten algo más que acceso a documentos clasificados."
        )
    },

    {
        "id": 13,
        "title": "El Daño Financiero",
        "coordinator_message_subject": "Contraloría — Irregularidades Presupuestarias por Departamento",
        "coordinator_message_body": (
            "Analista 734.\n\n"
            "La Contraloría detectó que varios departamentos superaron su presupuesto "
            "anual autorizado. Necesitamos un resumen por departamento.\n\n"
            "De la tabla 'transacciones', calcule para cada departamento:\n"
            "  · gasto_total: suma de todos los montos\n"
            "  · num_transacciones: cantidad de transacciones\n"
            "  · mayor_gasto: el monto más alto individual\n\n"
            "Agrupe por departamento. Ordene por gasto_total descendente.\n\n"
            "— Coordinadora Vera"
        ),
        "setup_sql": _DROPS + [
            "CREATE TABLE transacciones (id INTEGER PRIMARY KEY, departamento TEXT, "
            "concepto TEXT, monto INTEGER, fecha TEXT, aprobado_por_id INTEGER);",
            "INSERT INTO transacciones VALUES (1, 'Alta Dirección', 'Consultoría especializada', 850000, '2025-03-15', 4);",
            "INSERT INTO transacciones VALUES (2, 'Análisis de Datos', 'Material informático', 28000, '2025-02-10', 2);",
            "INSERT INTO transacciones VALUES (3, 'Alta Dirección', 'Software de vigilancia', 90000, '2025-04-20', 4);",
            "INSERT INTO transacciones VALUES (4, 'Infraestructura', 'Mantenimiento de red', 15000, '2025-01-30', 7);",
            "INSERT INTO transacciones VALUES (5, 'Consultoría Externa', 'Honorarios agentes', 220000, '2025-05-01', 4);",
            "INSERT INTO transacciones VALUES (6, 'Análisis de Datos', 'Formación', 12000, '2025-03-01', 6);",
            "INSERT INTO transacciones VALUES (7, 'Alta Dirección', 'Transporte seguro', 45000, '2025-05-10', 4);",
            "INSERT INTO transacciones VALUES (8, 'Archivo y Documentación', 'Digitalización', 8000, '2025-04-05', 5);",
            "INSERT INTO transacciones VALUES (9, 'Alta Dirección', 'Operación especial clasificada', 320000, '2025-06-01', 4);",
        ],
        "correct_query": (
            "SELECT departamento, SUM(monto) AS gasto_total, "
            "COUNT(*) AS num_transacciones, MAX(monto) AS mayor_gasto "
            "FROM transacciones "
            "GROUP BY departamento "
            "ORDER BY gasto_total DESC;"
        ),
        "evaluation_options": {
            "order_matters": True,
            "column_order_matters": True,
            "check_column_names": True
        },
        "hint": "Agrupa las transacciones y calcula varias estadisticas por grupo. | Use SUM, COUNT y MAX en el SELECT. GROUP BY departamento. Ordene por gasto_total DESC.",
        "success_message": (
            "Alta Dirección gastó 1.305.000 créditos en 4 transacciones.\n\n"
            "Su presupuesto anual autorizado era 200.000 créditos. "
            "Alguien aprobó el 652% del presupuesto de su propio departamento. "
            "Todas las transacciones de Alta Dirección fueron aprobadas por el mismo ID: el 4."
        )
    },

    {
        "id": 14,
        "title": "Aislando la Amenaza",
        "coordinator_message_subject": "Informe Prioritario — Casos de Acceso con Umbral Crítico",
        "coordinator_message_body": (
            "Analista 734.\n\n"
            "Necesito que filtre el informe de accesos. Esta vez quiero ver solo los "
            "casos que realmente importan: personas que hayan accedido a más de 2 "
            "documentos SECRETO.\n\n"
            "De la tabla 'registros_acceso', agrupe por empleado_nombre, cuente los "
            "accesos a clasificacion = 'SECRETO' y filtre con HAVING para mostrar "
            "solo quienes superen ese umbral.\n"
            "Muestre: empleado_nombre y total_accesos.\n"
            "Ordene por total_accesos descendente.\n\n"
            "— Coordinadora Vera"
        ),
        "setup_sql": _DROPS + [
            _CREATE_REGISTROS_ACCESO,
        ] + _INSERT_REGISTROS_ACCESO,
        "correct_query": (
            "SELECT empleado_nombre, COUNT(*) AS total_accesos "
            "FROM registros_acceso "
            "WHERE clasificacion = 'SECRETO' "
            "GROUP BY empleado_nombre "
            "HAVING COUNT(*) > 2 "
            "ORDER BY total_accesos DESC;"
        ),
        "evaluation_options": {
            "order_matters": True,
            "column_order_matters": True,
            "check_column_names": True
        },
        "hint": "Despues de agrupar, filtra los grupos que superen cierto umbral de conteo. | Despues del GROUP BY, agregue HAVING COUNT(*) > 2. HAVING actua sobre el resultado del GROUP BY.",
        "success_message": (
            "Tres casos prioritarios:\n\n"
            "  · Director Kael Umbra  — 6\n"
            "  · Agente Nova K        — 4\n"
            "  · Coordinadora Vera    — 3\n\n"
            "Los tres son parte del círculo de confianza del Director. "
            "Y la Coordinadora Vera —quien le pidió este informe— también figura en la lista."
        )
    },

    # ══════════════════════════════════════════════════════════════════════════
    # ACTO IV — EL INFORME CONSOLIDADO (Misión 15)
    # Concepto: Repaso integral (IN + fecha + GROUP BY + HAVING + LIMIT)
    # ══════════════════════════════════════════════════════════════════════════

    {
        "id": 15,
        "title": "Informe de Situación",
        "coordinator_message_subject": "URGENTE — Consolidado Final Antes de la Purga del Sistema",
        "coordinator_message_body": (
            "Analista 734. Rho.\n\n"
            "El tiempo se acaba. En menos de una hora el sistema borrará los logs.\n\n"
            "Necesito el informe consolidado de accesos críticos desde el 9 de junio. "
            "Solo clasificacion SECRETO o ULTRA-SECRETO. Solo quienes hayan accedido "
            "más de una vez. El top 5 por número de accesos.\n\n"
            "De 'registros_acceso', muestre:\n"
            "  empleado_nombre, clasificacion, COUNT(*) AS accesos, MAX(fecha) AS ultimo_acceso\n"
            "Filtros: clasificacion IN ('SECRETO', 'ULTRA-SECRETO') AND fecha > '2025-06-09'\n"
            "Agrupe por empleado_nombre y clasificacion.\n"
            "HAVING COUNT(*) > 1. Ordene por accesos DESC, empleado_nombre ASC. LIMIT 5.\n\n"
            "— Rho [última ventana disponible]"
        ),
        "setup_sql": _DROPS + [
            _CREATE_REGISTROS_ACCESO,
        ] + _INSERT_REGISTROS_ACCESO,
        "correct_query": (
            "SELECT empleado_nombre, clasificacion, "
            "COUNT(*) AS accesos, MAX(fecha) AS ultimo_acceso "
            "FROM registros_acceso "
            "WHERE clasificacion IN ('SECRETO', 'ULTRA-SECRETO') "
            "AND fecha > '2025-06-09' "
            "GROUP BY empleado_nombre, clasificacion "
            "HAVING COUNT(*) > 1 "
            "ORDER BY accesos DESC, empleado_nombre ASC "
            "LIMIT 5;"
        ),
        "evaluation_options": {
            "order_matters": True,
            "column_order_matters": True,
            "check_column_names": True
        },
        "hint": "Combina filtros, agrupamiento, condicion sobre el grupo y limite de filas. | Necesitas WHERE con IN y fecha, GROUP BY dos columnas, HAVING para el conteo, y LIMIT 5 al final.",
        "success_message": (
            "Informe consolidado. Los mismos tres nombres, los mismos documentos, la misma semana:\n\n"
            "  · Director Kael Umbra  — 6 accesos SECRETO (último: 14-Jun)\n"
            "  · Agente Nova K        — 3 accesos SECRETO (último: 12-Jun)\n"
            "  · Coordinadora Vera    — 3 accesos SECRETO (último: 11-Jun)\n\n"
            "Una coordinación no puede ser casualidad. Algo se estaba preparando."
        )
    },

    # ══════════════════════════════════════════════════════════════════════════
    # ACTO V — LAS PRUEBAS (Misiones 16–19)
    # Conceptos: Triple JOIN, subqueries, COUNT DISTINCT, LEFT JOIN complejo
    # ══════════════════════════════════════════════════════════════════════════

    {
        "id": 16,
        "title": "La Misma Noche",
        "coordinator_message_subject": "CIFRADO NIV.4 — Cruce Físico/Digital: 14-Jun-2025",
        "coordinator_message_body": (
            "Analista 734. Rho.\n\n"
            "Tengo la pieza que faltaba. Necesito que cruce tres tablas:\n"
            "quiénes accedieron a documentos SECRETO el 14 de junio, "
            "y dónde estaban físicamente ese día según el metro.\n\n"
            "Cruce 'empleados' (e) con 'registros_acceso' (ra) usando e.id = ra.empleado_id, "
            "y con 'registros_metro' (rm) usando e.tarjeta_metro = rm.tarjeta_id.\n\n"
            "Muestre: e.nombre, e.cargo, ra.documento_id, ra.clasificacion, "
            "ra.fecha AS fecha_acceso, rm.estacion_entrada, rm.timestamp_entrada AS hora_metro.\n\n"
            "Filtre: clasificacion = 'SECRETO' AND ra.fecha = '2025-06-14' AND rm.fecha = '2025-06-14'.\n"
            "Ordene por e.nombre ASC, ra.documento_id ASC.\n\n"
            "— Rho [CIFRADO ACTIVO]"
        ),
        "setup_sql": _DROPS + [
            _CREATE_EMPLEADOS,
        ] + _INSERT_EMPLEADOS + [
            _CREATE_REGISTROS_ACCESO,
        ] + _INSERT_REGISTROS_ACCESO + [
            _CREATE_REGISTROS_METRO,
        ] + _INSERT_REGISTROS_METRO,
        "correct_query": (
            "SELECT e.nombre, e.cargo, ra.documento_id, ra.clasificacion, "
            "ra.fecha AS fecha_acceso, rm.estacion_entrada, rm.timestamp_entrada AS hora_metro "
            "FROM empleados e "
            "JOIN registros_acceso ra ON e.id = ra.empleado_id "
            "JOIN registros_metro rm ON e.tarjeta_metro = rm.tarjeta_id "
            "WHERE ra.clasificacion = 'SECRETO' "
            "AND ra.fecha = '2025-06-14' "
            "AND rm.fecha = '2025-06-14' "
            "ORDER BY e.nombre ASC, ra.documento_id ASC;"
        ),
        "evaluation_options": {
            "order_matters": True,
            "column_order_matters": True,
            "check_column_names": True
        },
        "hint": "Necesitas cruzar tres fuentes de datos para verificar una coartada. | Una tres tablas: empleados JOIN registros_acceso JOIN registros_metro. Filtra por clasificacion y coincidencia de fechas.",
        "success_message": (
            "Resultado: dos personas el mismo día.\n\n"
            "  · Coordinadora Vera   — accedió al doc 2 (SECRETO) — estaba en el Ministerio a las 08:15\n"
            "  · Director Kael Umbra — accedió al doc 2 (SECRETO) — estaba en el Ministerio a las 08:00\n\n"
            "Ambos en el Ministerio, ambos accediendo al mismo documento (Protocolo Omega-7), "
            "con 15 minutos de diferencia. No fue casualidad. Estaban coordinando."
        )
    },


    {
        "id": 17,
        "title": "Los Contratos Fantasma",
        "coordinator_message_subject": "Contraloria — Contratos Sin Licitacion: Monto Acumulado por Proveedor",
        "coordinator_message_body": (
            "Analista 734.\n\n"
            "La Contraloria detecto contratos adjudicados sin proceso de licitacion abierta. "
            "Necesitamos identificar a quien aprobo contratos por mas de 100.000 creditos "
            "totales con un mismo proveedor.\n\n"
            "Tiene tres tablas:\n"
            "  'contratos' (c) — id, proveedor_id, monto, fecha, aprobado_por\n"
            "  'proveedores' (p) — id, nombre, email\n"
            "  'empleados' (e) — id, nombre, cargo, ...\n\n"
            "Una las tres. Muestre: p.nombre AS proveedor, e.nombre AS aprobador, "
            "COUNT(c.id) AS num_contratos, SUM(c.monto) AS monto_total.\n"
            "Agrupe por proveedor y aprobador. HAVING SUM > 100000.\n"
            "Ordene por monto_total DESC, proveedor ASC.\n\n"
            "— Coordinadora Vera"
        ),
        "setup_sql": _DROPS + [
            _CREATE_EMPLEADOS,
        ] + _INSERT_EMPLEADOS + [
            "CREATE TABLE proveedores (id INTEGER PRIMARY KEY, nombre TEXT, email TEXT);",
            "INSERT INTO proveedores VALUES (1, 'TechSecure S.A.', 'techsecure@novaris.gob');",
            "INSERT INTO proveedores VALUES (2, 'Vigilancia Total Ltda.', 'vt@vt.nv');",
            "INSERT INTO proveedores VALUES (3, 'Consultores Independ.', 'ci@consult.nv');",
            "INSERT INTO proveedores VALUES (4, 'Infraestructura Publica', 'infra@pub.nv');",
            "CREATE TABLE contratos (id INTEGER PRIMARY KEY, proveedor_id INTEGER, "
            "monto INTEGER, fecha TEXT, aprobado_por INTEGER);",
            "INSERT INTO contratos VALUES (1, 1, 90000, '2025-04-20', 4);",
            "INSERT INTO contratos VALUES (2, 2, 320000, '2025-06-01', 4);",
            "INSERT INTO contratos VALUES (3, 1, 850000, '2025-03-15', 4);",
            "INSERT INTO contratos VALUES (4, 3, 220000, '2025-05-01', 4);",
            "INSERT INTO contratos VALUES (5, 4, 15000, '2025-01-30', 7);",
            "INSERT INTO contratos VALUES (6, 2, 45000, '2025-05-10', 2);",
            "INSERT INTO contratos VALUES (7, 3, 28000, '2025-02-10', 6);",
        ],
        "correct_query": (
            "SELECT p.nombre AS proveedor, e.nombre AS aprobador, "
            "COUNT(c.id) AS num_contratos, SUM(c.monto) AS monto_total "
            "FROM contratos c "
            "JOIN proveedores p ON c.proveedor_id = p.id "
            "JOIN empleados e ON c.aprobado_por = e.id "
            "GROUP BY p.nombre, e.nombre "
            "HAVING SUM(c.monto) > 100000 "
            "ORDER BY monto_total DESC, proveedor ASC;"
        ),
        "evaluation_options": {
            "order_matters": True,
            "column_order_matters": True,
            "check_column_names": True
        },
        "hint": "Busca patrones de contratacion agrupando por proveedor y quien los aprobo. | Una contratos con proveedores y empleados. Agrupe por proveedor y aprobador, filtre con HAVING SUM mayor a 100000.",
        "success_message": (
            "1.480.000 creditos en contratos aprobados por una sola persona:\n\n"
            "  · TechSecure S.A.        — 2 contratos — 940.000 creditos\n"
            "  · Vigilancia Total Ltda. — 1 contrato  — 320.000 creditos\n"
            "  · Consultores Independ.  — 1 contrato  — 220.000 creditos\n\n"
            "El Reglamento de Compras exige licitacion abierta para montos superiores a 50.000. "
            "Todos estos contratos fueron aprobados por el Director Kael Umbra, sin excepcion."
        )
    },

    {
        "id": 18,
        "title": "El Testigo Silencioso",
        "coordinator_message_subject": "CIFRADO NIV.4 — Operativos No Registrados en el Metro",
        "coordinator_message_body": (
            "Analista 734. Rho.\n\n"
            "Hay personas en el metro ese dia que no existen en nuestros registros. "
            "Ninguna tarjeta de la UEI deberia ser anonima.\n\n"
            "Use una subconsulta: de 'registros_metro', filtre fecha '2025-06-14' "
            "y donde tarjeta_id NOT IN (SELECT tarjeta_metro FROM empleados "
            "WHERE tarjeta_metro IS NOT NULL).\n\n"
            "Muestre: tarjeta_id, estacion_entrada, timestamp_entrada.\n"
            "Ordene por timestamp_entrada ASC.\n\n"
            "Son los que nadie registro. Los que nadie queria que encontraramos.\n\n"
            "— Rho"
        ),
        "setup_sql": _DROPS + [
            _CREATE_EMPLEADOS,
        ] + _INSERT_EMPLEADOS + [
            _CREATE_REGISTROS_METRO,
        ] + _INSERT_REGISTROS_METRO,
        "correct_query": (
            "SELECT tarjeta_id, estacion_entrada, timestamp_entrada "
            "FROM registros_metro "
            "WHERE fecha = '2025-06-14' "
            "AND tarjeta_id NOT IN ("
            "SELECT tarjeta_metro FROM empleados WHERE tarjeta_metro IS NOT NULL"
            ") "
            "ORDER BY timestamp_entrada ASC;"
        ),
        "evaluation_options": {
            "order_matters": True,
            "column_order_matters": True,
            "check_column_names": True
        },
        "hint": "Identifica tarjetas de transporte que no pertenecen a ningun empleado. | Use NOT IN con una subconsulta que seleccione las tarjetas de empleados. Ojo con los valores nulos.",
        "success_message": (
            "Dos operativos sin identidad registrada:\n\n"
            "  · SUBE-EXT1 — Ministerio       — 07:55  (5 min antes que el Director)\n"
            "  · SUBE-EXT2 — Archivo Nacional — 21:30  (de noche, sin salida)\n\n"
            "No figuran en ninguna base de datos de la UEI. "
            "Alguien los envio. Alguien sabia que iban a estar ahi. "
            "Y ese alguien tenia acceso para borrar sus identidades del sistema."
        )
    },

    {
        "id": 19,
        "title": "El Perfil Completo",
        "coordinator_message_subject": "CIFRADO NIV.4 — Ultima Pieza: Accesos + Ordenes de Vigilancia",
        "coordinator_message_body": (
            "Analista 734. Rho.\n\n"
            "Ultima pieza. Necesito que cruce quien accedio a documentos clasificados "
            "con cuantas ordenes de vigilancia emitio esa misma persona.\n\n"
            "Tablas: 'empleados' (e), 'registros_acceso' (ra), 'ordenes_vigilancia' (ov).\n\n"
            "JOIN registros_acceso ON e.id = ra.empleado_id.\n"
            "LEFT JOIN ordenes_vigilancia ON ov.emitido_por = e.id.\n"
            "WHERE ra.clasificacion IN ('SECRETO', 'ULTRA-SECRETO').\n\n"
            "Muestre: e.nombre, e.cargo, "
            "COUNT(DISTINCT ra.documento_id) AS docs_secreto, "
            "COUNT(DISTINCT ov.id) AS ordenes_emitidas.\n"
            "Agrupe por e.id, e.nombre, e.cargo.\n"
            "Ordene por docs_secreto DESC, ordenes_emitidas DESC.\n\n"
            "— Rho [ULTIMA CONEXION]"
        ),
        "setup_sql": _DROPS + [
            _CREATE_EMPLEADOS,
        ] + _INSERT_EMPLEADOS + [
            _CREATE_REGISTROS_ACCESO,
        ] + _INSERT_REGISTROS_ACCESO + [
            "CREATE TABLE ordenes_vigilancia (id INTEGER PRIMARY KEY, objetivo_id INTEGER, "
            "emitido_por INTEGER, fecha_inicio TEXT, status TEXT, razon TEXT);",
            "INSERT INTO ordenes_vigilancia VALUES (1, 3, 4, '2025-04-01', 'ACTIVA', 'Contactos externos no autorizados');",
            "INSERT INTO ordenes_vigilancia VALUES (2, 5, 4, '2025-04-15', 'ACTIVA', 'Acceso irregular al archivo');",
            "INSERT INTO ordenes_vigilancia VALUES (3, 1, 4, '2025-05-12', 'ACTIVA', 'Evaluacion de lealtad — Protocolo SECUELAS');",
            "INSERT INTO ordenes_vigilancia VALUES (4, 2, 4, '2024-12-01', 'CERRADA', 'Sospecha de filtracion');",
            "INSERT INTO ordenes_vigilancia VALUES (5, 4, 2, '2025-06-01', 'ACTIVA', 'Auditoria independiente solicitada');",
            "INSERT INTO ordenes_vigilancia VALUES (6, 7, 4, '2025-03-20', 'ACTIVA', 'Actividad tecnica fuera de horario');",
        ],
        "correct_query": (
            "SELECT e.nombre, e.cargo, "
            "COUNT(DISTINCT ra.documento_id) AS docs_secreto, "
            "COUNT(DISTINCT ov.id) AS ordenes_emitidas "
            "FROM empleados e "
            "JOIN registros_acceso ra ON e.id = ra.empleado_id "
            "LEFT JOIN ordenes_vigilancia ov ON ov.emitido_por = e.id "
            "WHERE ra.clasificacion IN ('SECRETO', 'ULTRA-SECRETO') "
            "GROUP BY e.id, e.nombre, e.cargo "
            "ORDER BY docs_secreto DESC, ordenes_emitidas DESC;"
        ),
        "evaluation_options": {
            "order_matters": True,
            "column_order_matters": True,
            "check_column_names": True
        },
        "hint": "Cuenta accesos a documentos por empleado, incluyendo quienes vigilaron. | Use JOIN registros_acceso y LEFT JOIN ordenes_vigilancia. Use COUNT DISTINCT para evitar duplicados.",
        "success_message": (
            "El perfil completo:\n\n"
            "  · Director Kael Umbra  — 3 docs unicos — 5 ordenes emitidas\n"
            "  · Coordinadora Vera    — 3 docs unicos — 1 orden emitida\n"
            "  · Agente Nova K        — 3 docs unicos — 0 ordenes emitidas\n\n"
            "Umbra accedio a tantos documentos clasificados como sus subordinados, "
            "pero ademas emitio 5 ordenes de vigilancia sobre su propio equipo.\n\n"
            "La orden 3 tiene como objetivo el ID 1. Eso es usted, Analista 734.\n"
            "Razon registrada: 'Evaluacion de lealtad — Protocolo SECUELAS'."
        )
    },

    {
        "id": 20,
        "title": "Protocolo SECUELAS: El Veredicto Final",
        "coordinator_message_subject": "PURGA DEL SISTEMA EN 60 SEGUNDOS — COMPILE EL INFORME AHORA",
        "coordinator_message_body": (
            "Analista 734.\n\n"
            "Ya lo sabe todo.\n\n"
            "El Protocolo SECUELAS era una trampa de lealtad. Cada consulta que ejecuto "
            "fue monitoreada. Usted era el objetivo desde el primer dia.\n\n"
            "Pero tambien es quien recopilo las pruebas.\n\n"
            "En la tabla 'evidencias' estan registradas las violaciones al codigo de la Republica. "
            "Compile el informe final del Director General antes de que el sistema se purgue.\n\n"
            "Una 'evidencias' (ev) con 'empleados' (e) usando ev.actor = e.nombre.\n"
            "Filtre donde e.cargo = 'Director General'.\n"
            "Agrupe por ev.tipo_violacion. Muestre:\n"
            "  tipo_violacion, COUNT(*) AS num_casos,\n"
            "  MIN(ev.fecha) AS primera_ocurrencia, MAX(ev.fecha) AS ultima_ocurrencia.\n"
            "Ordene por num_casos DESC, tipo_violacion ASC.\n\n"
            "Lo que haga con esto es su decision."
        ),
        "setup_sql": _DROPS + [
            _CREATE_EMPLEADOS,
        ] + _INSERT_EMPLEADOS + [
            "CREATE TABLE evidencias (id INTEGER PRIMARY KEY, actor TEXT, "
            "tipo_violacion TEXT, fecha TEXT, detalles TEXT);",
            "INSERT INTO evidencias VALUES (1, 'Director Kael Umbra', 'Vigilancia Ilegal', '2025-04-01', 'Orden s/aprobacion sobre Nova K');",
            "INSERT INTO evidencias VALUES (2, 'Director Kael Umbra', 'Malversacion de Fondos', '2025-03-15', 'Contrato 850000 s/licitacion');",
            "INSERT INTO evidencias VALUES (3, 'Director Kael Umbra', 'Vigilancia Ilegal', '2025-04-15', 'Vigilancia s/causa sobre Archivista Rho');",
            "INSERT INTO evidencias VALUES (4, 'Director Kael Umbra', 'Destruccion de Evidencia', '2025-06-13', 'Borrado de logs a Operacion SECUELAS');",
            "INSERT INTO evidencias VALUES (5, 'Director Kael Umbra', 'Vigilancia Ilegal', '2025-05-12', 'Orden sobre Analista 734');",
            "INSERT INTO evidencias VALUES (6, 'Director Kael Umbra', 'Abuso de Autoridad', '2025-03-20', 'Sistema UEI usado para fines personales');",
            "INSERT INTO evidencias VALUES (7, 'Director Kael Umbra', 'Malversacion de Fondos', '2025-06-01', '320000 en operacion no autorizada');",
            "INSERT INTO evidencias VALUES (8, 'Coordinadora Vera', 'Omision de Denuncia', '2025-06-14', 'Conocia irregularidades, no reporto');",
            "INSERT INTO evidencias VALUES (9, 'Agente Nova K', 'Acceso No Autorizado', '2025-06-10', 'Acceso a docs fuera de su nivel');",
        ],
        "correct_query": (
            "SELECT ev.tipo_violacion, COUNT(*) AS num_casos, "
            "MIN(ev.fecha) AS primera_ocurrencia, MAX(ev.fecha) AS ultima_ocurrencia "
            "FROM evidencias ev "
            "JOIN empleados e ON ev.actor = e.nombre "
            "WHERE e.cargo = 'Director General' "
            "GROUP BY ev.tipo_violacion "
            "ORDER BY num_casos DESC, ev.tipo_violacion ASC;"
        ),
        "evaluation_options": {
            "order_matters": True,
            "column_order_matters": True,
            "check_column_names": True
        },
        "hint": "Cruza accesos a documentos con alertas de seguridad para el mismo dia. | Una evidencias con empleados por nombre. Filtre por cargo. Use MIN y MAX sobre fecha para el rango.",
        "success_message": (
            "Informe transmitido al Tribunal de Control Independiente.\n\n"
            "  · Vigilancia Ilegal        — 3 casos — (01-Abr a 12-May-2025)\n"
            "  · Malversacion de Fondos   — 2 casos — (15-Mar a 01-Jun-2025)\n"
            "  · Abuso de Autoridad       — 1 caso  — (20-Mar-2025)\n"
            "  · Destruccion de Evidencia — 1 caso  — (13-Jun-2025)\n\n"
            "El Protocolo SECUELAS era una trampa de lealtad. Usted era el objetivo. "
            "Pero tambien fue quien recopilo las pruebas que lo detuvieron.\n\n"
            "— FIN DE LA SIMULACION —"
        )
    },
]
