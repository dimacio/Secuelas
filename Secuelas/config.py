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
            len(results) >= 1 and  # Debe haber al menos un resultado esperado
            # CONDICIÓN PRINCIPAL: Todos los resultados deben ser de PROYECTO_QUIMERA y cumplir la fecha
            all(
                r.get('document_token_fk') == 'PROYECTO_QUIMERA' and
                (
                    datetime.datetime.strptime(str(r.get('access_timestamp')).split('.')[0], '%Y-%m-%d %H:%M:%S')
                    if isinstance(r.get('access_timestamp'), (str, datetime.datetime))
                    else datetime.datetime.min
                ) > datetime.datetime(2025, 5, 19, 10, 0, 0)
                for r in results
            )
        ),
        "hint": "Consulte la tabla 'document_access_logs'. Filtre por la columna 'document_token_fk' para el documento y por 'access_timestamp' para la fecha/hora. Recuerde que las fechas y horas deben compararse cuidadosamente (formato 'YYYY-MM-DD HH:MM:SS').", # <--- PISTA ACTUALIZADA
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
    # En config.py
# ... (Misiones 1 a 4 permanecen con pequeños ajustes si es necesario) ...

# Ejemplo para la misión 3 (solo para ilustrar que el document_id ahora es un token):
# La lambda solution_check para la misión 3 debería seguir funcionando
# ya que accede a row['document_id'] (que ahora es document_token_fk en la DB pero SQLAlchemy podría mapearlo así o
# deberías usar row['document_token_fk']). Verifica esto en tus resultados.
# Si usas dict(zip(column_names, row)), el nombre de la columna será 'document_token_fk'.
# Por lo tanto, la comprobación para la misión 3 debería ser:
# any(row['document_token_fk'] == 'PROYECTO_QUIMERA' and ...
# y expected_table seguiría siendo "document_access_logs"

# Misión 5 (REDISEÑADA - Ejemplo)
    {
        "id": 5,
        "title": "Investigación de Documento Específico",
        "coordinator_message_subject": "Solicitud de Detalles: MANUAL_UEI_001",
        "coordinator_message_body": (
            "Analista, necesitamos que recupere toda la información disponible sobre el documento con el token 'MANUAL_UEI_001'.\n"
            "Presente todos sus atributos registrados en la base de datos de documentos."
        ),
        "expected_table": "documents", # Ahora buscamos en la tabla 'documents'
        "solution_check": lambda results: (
            results is not None and
            len(results) == 1 and
            results[0]['document_token'] == 'MANUAL_UEI_001' and
            'title' in results[0] and 
            'description' in results[0] # Verificar que otros campos esperados estén presentes
        ),
        "hint": "Consulte la tabla 'documents'. Filtre por la columna 'document_token'. Seleccione todas las columnas para ver todos los atributos.",
        "success_message": "Información del documento 'MANUAL_UEI_001' recuperada y archivada. Buen trabajo."
    },
    # En config.py, después de la misión 5 o donde corresponda

    {
        "id": 6, # Siguiente ID disponible
        "title": "Auditoría Cruzada: Accesos a 'PROYECTO_QUIMERA'",
        "coordinator_message_subject": "Directiva de Auditoría Avanzada XR-003",
        "coordinator_message_body": (
            "Analista, se requiere un análisis más profundo de los accesos al 'PROYECTO_QUIMERA'.\n"
            "Presente un informe que liste el nombre del empleado, su cargo, y la fecha y hora del acceso para todos los registros relacionados con 'PROYECTO_QUIMERA'.\n"
            "Necesitamos cruzar información de las tablas de empleados y los registros de acceso a documentos."
        ),
        "expected_table": "employees, document_access_logs, documents", # Tablas involucradas
        "solution_check": lambda results: (
            results is not None and
            len(results) >= 3 and # Basado en tus datos de siembra para PROYECTO_QUIMERA
            all('name' in row and 'position' in row and 'access_timestamp' in row for row in results) and
            # Verificar que los datos sean consistentes con un JOIN exitoso
            # (Esta es una comprobación simplificada, podrías hacerla más robusta)
            any(row['name'] == 'Supervisor Nex' for row in results) and
            any(row['name'] == 'Agente Externo K' for row in results)
        ),
        "hint": "Utilice JOIN (o INNER JOIN) para combinar 'employees' con 'document_access_logs' usando 'employees.id' y 'document_access_logs.employee_id'. Luego, filtre los resultados donde 'document_access_logs.document_token_fk' sea 'PROYECTO_QUIMERA'. Seleccione 'employees.name', 'employees.position', y 'document_access_logs.access_timestamp'.",
        "success_message": "Informe de auditoría cruzada para 'PROYECTO_QUIMERA' completado. Las conexiones se están volviendo más claras."
    }
]