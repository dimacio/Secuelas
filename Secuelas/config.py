import datetime

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
            any(row['name'] == 'Supervisor Nex' for row in results)
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
            len(results) >= 1 and 
            any(row['document_id'] == 'PROYECTO_QUIMERA' and 
                (datetime.datetime.strptime(str(row['access_timestamp']).split('.')[0], '%Y-%m-%d %H:%M:%S') if isinstance(row.get('access_timestamp'), (str, datetime.datetime)) else datetime.datetime.min) > datetime.datetime(2025, 5, 19, 10, 0, 0) and
                row['employee_id'] == 3 
                for row in results)
        ),
        "hint": "Consulte la tabla 'document_access_logs'. Filtre por 'document_id' y 'access_timestamp'. Recuerde que las fechas y horas deben compararse cuidadosamente (formato 'YYYY-MM-DD HH:MM:SS').",
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
        "hint": "Consulte la tabla 'employees'. Filtre por la columna 'security_clearance' para valores mayores a 3. Puede que necesite ser más específico para aislar al individuo correcto si hay varios con alta autorización.",
        "success_message": "Información obtenida. La discreción es su mejor aliada. Mantenga estos datos en reserva."
    },
    {
        "id": 5,
        "title": "El archivo secreto",
        "coordinator_message_subject": "Mensaje perdido",
        "coordinator_message_body": (
            "Parece que llegó un mensaje por error\n"
            "REMITENTE: 'Desconocido'\n"
            "MENSAJE: 'Busque el archive"
        ),
        "expected_table": "archive",
        "solution_check": lambda results: (
            results is not None and
            len(results) == 1 and
            results[0]['document_id'] == 'MANUAL_UEI_001' 
        ),
        "hint": "SELECT * FROM archive",
        "success_message": "funciona!"
    }

]