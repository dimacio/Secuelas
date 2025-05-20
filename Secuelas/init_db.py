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

        # Sembrar datos para DocumentAccessLog si la tabla está vacía
        if not models.DocumentAccessLog.query.first():
            print("initialize_database: Sembrando logs de acceso...")
            access_logs_data = [
                models.DocumentAccessLog(employee_id=1, document_id="MANUAL_UEI_001", action="VIEW", access_timestamp=datetime.datetime(2025, 5, 19, 9, 15, 0), remarks="Acceso estándar de orientación."),
                models.DocumentAccessLog(employee_id=2, document_id="PROYECTO_QUIMERA", action="VIEW", access_timestamp=datetime.datetime(2025, 5, 19, 9, 30, 0), remarks="Revisión de Supervisor."),
                models.DocumentAccessLog(employee_id=5, document_id="REGISTRO_HISTORICO_77B", action="ARCHIVE", access_timestamp=datetime.datetime(2025, 5, 19, 9, 45, 0)),
                models.DocumentAccessLog(employee_id=3, document_id="PROYECTO_QUIMERA", action="CLASSIFIED_VIEW", access_timestamp=datetime.datetime(2025, 5, 19, 11, 5, 30), remarks="Acceso no programado. Requiere seguimiento."),
                models.DocumentAccessLog(employee_id=1, document_id="PROYECTO_QUIMERA", action="VIEW", access_timestamp=datetime.datetime(2025, 5, 19, 14, 20, 0), remarks="Acceso autorizado para tarea de auditoría."),
                models.DocumentAccessLog(employee_id=4, document_id="PROYECTO_QUIMERA", action="VIEW", access_timestamp=datetime.datetime(2025, 5, 18, 17, 0, 0), remarks="Revisión Directiva."),
            ]
            db.session.bulk_save_objects(access_logs_data)
            db.session.commit()
            print("initialize_database: Logs de acceso sembrados.")
        else:
            print("initialize_database: Logs de acceso ya existen, no se siembran.")
        print("initialize_database: Finalizado.")

        # Sembrar datos para Archive si la tabla está vacía TEST
        if not models.Archive.query.first():
            print("initialize_database: Sembrando archivo...")
            access_logs_data = [
                models.Archive(archive_id=1, document_id="MANUAL_UEI_001", department="Unidad de Escrutinio Informativo", content = "Siempre hay que cumplir las misiones, nunca hay que cuestionar las misiones"),
                 ]
            db.session.bulk_save_objects(access_logs_data)
            db.session.commit()
            print("initialize_database: Logs de acceso archivo.")
        else:
            print("initialize_database: Logs de acceso ya existen, no se siembran.")
        print("initialize_database: Finalizado.")
