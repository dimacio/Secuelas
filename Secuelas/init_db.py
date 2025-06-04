# Secuelas/init_db.py
from sqlalchemy import text, exc, asc
from extensions import db
from models import MissionDefinitionDB # Importar el nuevo modelo
import json

def execute_sql_script(db_session, sql_statements):
    """Ejecuta una lista de sentencias SQL dentro de la sesión dada."""
    if not sql_statements:
        print("execute_sql_script: No hay sentencias SQL para ejecutar.")
        return
    for stmt_index, stmt in enumerate(sql_statements):
        if stmt and stmt.strip():
            try:
                print(f"execute_sql_script: Ejecutando stmt {stmt_index + 1}/{len(sql_statements)}: {stmt[:100]}...")
                db_session.execute(text(stmt))
            except exc.SQLAlchemyError as e:
                print(f"Error ejecutando SQL de configuración: {stmt} - {e}")
                db_session.rollback()
                raise
            except Exception as e:
                print(f"Error inesperado ejecutando SQL de configuración: {stmt} - {e}")
                db_session.rollback()
                raise
    try:
        db_session.commit()
        print("execute_sql_script: Commit exitoso de las sentencias SQL.")
    except exc.SQLAlchemyError as e:
        print(f"Error haciendo commit de las sentencias SQL: {e}")
        db_session.rollback()
        raise
    except Exception as e:
        print(f"Error inesperado haciendo commit de las sentencias SQL: {e}")
        db_session.rollback()
        raise

def load_initial_missions_from_config_to_db(db_session):
    """
    Carga las misiones desde el archivo config.py (si existe la variable MISSIONS)
    a la tabla MissionDefinitionDB si la tabla está vacía.
    """
    try:
        from config import MISSIONS as MISSIONS_FROM_CONFIG 
    except ImportError:
        print("load_initial_missions: No se pudo importar MISSIONS desde config.py.")
        return
    
    if not MISSIONS_FROM_CONFIG:
        print("load_initial_missions: No hay misiones definidas en config.py para cargar.")
        return

    if MissionDefinitionDB.query.first() is not None:
        print("load_initial_missions: La tabla 'mission_definitions' ya contiene datos. No se cargarán misiones desde config.py.")
        return

    print(f"load_initial_missions: Cargando {len(MISSIONS_FROM_CONFIG)} misiones desde config.py a la base de datos...")
    for mission_data in MISSIONS_FROM_CONFIG:
        try:
            setup_sql_str = ";\n".join(mission_data.get('setup_sql', []))

            new_mission_db = MissionDefinitionDB(
                id=mission_data['id'],
                title=mission_data['title'],
                coordinator_message_subject=mission_data['coordinator_message_subject'],
                coordinator_message_body=mission_data['coordinator_message_body'],
                setup_sql_script=setup_sql_str,
                correct_query_script=mission_data['correct_query'],
                evaluation_options_json=json.dumps(mission_data['evaluation_options']),
                hint=mission_data.get('hint'),
                success_message=mission_data['success_message']
            )
            db_session.add(new_mission_db)
            print(f"  Añadiendo Misión ID {mission_data['id']}: {mission_data['title']}")
        except Exception as e:
            print(f"  Error al preparar la misión ID {mission_data['id']} para la base de datos: {e}")
            db_session.rollback() 
            return 

    try:
        db_session.commit()
        print("load_initial_missions: Misiones iniciales cargadas exitosamente a la base de datos.")
    except Exception as e:
        db_session.rollback()
        print(f"load_initial_missions: Error al hacer commit de las misiones iniciales: {e}")

# This is the correctly named function that app.py expects
def initialize_app_database(app_context): 
    """
    Inicializa la base de datos de la aplicación:
    1. Crea todas las tablas definidas en models.py (incluida MissionDefinitionDB).
    2. Carga las misiones iniciales desde config.py a la BD si la tabla de misiones está vacía.
    3. Configura la base de datos para la primera misión del juego (si existe alguna misión).
    """
    with app_context.app_context():
        print("initialize_app_database: Iniciando...")
        
        print("initialize_app_database: Creando todas las tablas definidas en models.py...")
        db.create_all() 
        print("initialize_app_database: Tablas creadas (o ya existían).")

        load_initial_missions_from_config_to_db(db.session)

        first_mission_from_db = MissionDefinitionDB.query.filter_by(is_active=True).order_by(asc(MissionDefinitionDB.id)).first()
        
        if first_mission_from_db:
            print(f"initialize_app_database: Configurando entorno para la primera misión (ID: {first_mission_from_db.id}) desde la BD...")
            try:
                execute_sql_script(db.session, first_mission_from_db.setup_sql)
                print(f"initialize_app_database: Entorno para la Misión {first_mission_from_db.id} configurado.")
            except Exception as e:
                print(f"initialize_app_database: Error configurando el entorno para la primera misión desde la BD: {e}")
        else:
            print("initialize_app_database: No hay misiones activas en la base de datos para configurar el entorno inicial del juego.")
        
        print("initialize_app_database: Finalizado.")
