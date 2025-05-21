from extensions import db
import models # Importar para que SQLAlchemy conozca los modelos para db.create_all()
import datetime # Necesario para los datos iniciales de Employee y DocumentAccessLog

def initialize_database(app_context):
    """
    Crea las tablas de la base de datos y siembra los datos iniciales
    si las tablas están vacías. Se ejecuta dentro del contexto de la aplicación.
    """
    with app_context.app_context(): # Asegura que las operaciones de BD se hagan con el contexto correcto
        print("initialize_database: Creando todas las tablas...")
        db.create_all()
        print("initialize_database: Tablas creadas (o ya existían).")

        # Sembrar datos para Empleados si la tabla está vacía
        if not models.Employee.query.first():
            print("initialize_database: Sembrando empleados...")
            employees_data = [
                models.Employee(id=1, name="Analista 734 (Usted)", department="Unidad de Escrutinio Informativo", position="Analista de Datos Jr.", security_clearance=2, hire_date=datetime.date(2025, 5, 10)),
                models.Employee(id=2, name="Supervisor Nex", department="Unidad de Escrutinio Informativo", position="Supervisor de Analistas", security_clearance=3, hire_date=datetime.date(2023, 2, 15)),
                models.Employee(id=3, name="Agente Externo K", department="Consultores Externos", position="Especialista en Seguridad de Datos", security_clearance=4, hire_date=datetime.date(2024, 11, 1)),
                models.Employee(id=4, name="Director General Umbra", department="Alta Dirección", position="Director General", security_clearance=5, hire_date=datetime.date(2010, 1, 5)),
                models.Employee(id=5, name="Técnico de Archivos Rho", department="Archivo Central", position="Archivista Principal", security_clearance=2, hire_date=datetime.date(2018, 7, 22)),
            ]
            db.session.bulk_save_objects(employees_data)
            db.session.commit()
            print("initialize_database: Empleados sembrados.")
        else:
            print("initialize_database: Empleados ya existen, no se siembran.")

          # NUEVO: Sembrar datos para Documentos si la tabla está vacía
        if not models.Document.query.first():
            print("initialize_database: Sembrando documentos...")
            documents_data = [
                models.Document(document_token="MANUAL_UEI_001", title="Manual de Orientación UEI", description="Procedimientos estándar y directivas para nuevos analistas.", classification_level=1, creation_date=datetime.datetime(2025, 1, 10)),
                models.Document(document_token="PROYECTO_QUIMERA", title="Proyecto Quimera - Ultrasecreto", description="Investigación y Desarrollo - Fase Preliminar.", classification_level=5, creation_date=datetime.datetime(2024, 6, 15)),
                models.Document(document_token="REGISTRO_HISTORICO_77B", title="Registro Histórico 77B - Archivos Clasificados", description="Incidente de seguridad, sector Gamma-7.", classification_level=4, creation_date=datetime.datetime(2023, 3, 22)),
                models.Document(document_token="PROTOCOLO_EVAC_ALFA", title="Protocolo de Evacuación Alfa", description="Procedimientos de emergencia para el Sitio Alfa.", classification_level=3, creation_date=datetime.datetime(2025, 2, 1))
            ]
            db.session.bulk_save_objects(documents_data)
            db.session.commit()
            print("initialize_database: Documentos sembrados.")
        else:
            print("initialize_database: Documentos ya existen, no se siembran.")

        # Sembrar datos para DocumentAccessLog (ACTUALIZADO)
        if not models.DocumentAccessLog.query.first():
            print("initialize_database: Sembrando logs de acceso...")
            # Asegúrate de que los employee_id existen y los document_token_fk coinciden con los tokens en la tabla 'documents'
            access_logs_data = [
                models.DocumentAccessLog(employee_id=1, document_token_fk="MANUAL_UEI_001", action="VIEW", access_timestamp=datetime.datetime(2025, 5, 19, 9, 15, 0), remarks="Acceso estándar de orientación."),
                models.DocumentAccessLog(employee_id=2, document_token_fk="PROYECTO_QUIMERA", action="VIEW", access_timestamp=datetime.datetime(2025, 5, 19, 9, 30, 0), remarks="Revisión de Supervisor."),
                models.DocumentAccessLog(employee_id=5, document_token_fk="REGISTRO_HISTORICO_77B", action="ARCHIVE_VIEW", access_timestamp=datetime.datetime(2025, 5, 19, 9, 45, 0)), # Cambié 'ARCHIVE' a 'ARCHIVE_VIEW' por claridad
                models.DocumentAccessLog(employee_id=3, document_token_fk="PROYECTO_QUIMERA", action="CLASSIFIED_VIEW", access_timestamp=datetime.datetime(2025, 5, 19, 11, 5, 30), remarks="Acceso no programado. Requiere seguimiento."),
                models.DocumentAccessLog(employee_id=1, document_token_fk="PROYECTO_QUIMERA", action="VIEW", access_timestamp=datetime.datetime(2025, 5, 19, 14, 20, 0), remarks="Acceso autorizado para tarea de auditoría."),
                models.DocumentAccessLog(employee_id=4, document_token_fk="PROYECTO_QUIMERA", action="VIEW", access_timestamp=datetime.datetime(2025, 5, 18, 17, 0, 0), remarks="Revisión Directiva."),
                models.DocumentAccessLog(employee_id=2, document_token_fk="PROTOCOLO_EVAC_ALFA", action="REVIEW", access_timestamp=datetime.datetime(2025, 5, 20, 10, 0, 0), remarks="Revisión de protocolo de seguridad.")
            ]
            db.session.bulk_save_objects(access_logs_data)
            db.session.commit()
            print("initialize_database: Logs de acceso sembrados.")
        else:
            print("initialize_database: Logs de acceso ya existen, no se siembran.")
        # Eliminar la siembra para la tabla Archive
        # if not models.Archive.query.first(): ... (todo este bloque se elimina)

    print("initialize_database: Finalizado.")