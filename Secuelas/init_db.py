# Secuelas/init_db.py
from sqlalchemy import text, exc
from extensions import db
# No se necesita importar 'models' aquí si setup_sql crea las tablas.
# No se necesita 'datetime' aquí.

def execute_sql_script(db_session, sql_statements):
    """Ejecuta una lista de sentencias SQL dentro de la sesión dada."""
    if not sql_statements:
        print("execute_sql_script: No hay sentencias SQL para ejecutar.")
        return
    for stmt_index, stmt in enumerate(sql_statements):
        if stmt and stmt.strip():  # Asegurar que no esté vacía
            try:
                print(f"execute_sql_script: Ejecutando stmt {stmt_index + 1}/{len(sql_statements)}: {stmt[:100]}...")
                db_session.execute(text(stmt))
            except exc.SQLAlchemyError as e: # Captura errores específicos de SQLAlchemy/DB
                print(f"Error ejecutando SQL de configuración: {stmt} - {e}")
                db_session.rollback() # Importante revertir en caso de error en una transacción
                raise  # Re-lanzar para señalar el fallo de configuración al llamador
            except Exception as e: # Captura otros posibles errores
                print(f"Error inesperado ejecutando SQL de configuración: {stmt} - {e}")
                db_session.rollback()
                raise
    try:
        db_session.commit() # Commit al final si todas las sentencias fueron exitosas
        print("execute_sql_script: Commit exitoso de las sentencias SQL.")
    except exc.SQLAlchemyError as e:
        print(f"Error haciendo commit de las sentencias SQL: {e}")
        db_session.rollback()
        raise
    except Exception as e:
        print(f"Error inesperado haciendo commit de las sentencias SQL: {e}")
        db_session.rollback()
        raise


def initialize_first_mission_db(app_context):
    """
    Configura la base de datos para la primera misión o un estado por defecto.
    Esto reemplaza la siembra de datos anterior.
    """
    # Importar MISSIONS aquí para evitar dependencia circular en la carga del módulo
    from config import MISSIONS
    
    # Asegura que las operaciones de BD se hagan con el contexto correcto de la aplicación
    with app_context.app_context():
        print("initialize_first_mission_db: Configurando base de datos para la primera misión...")
        
        # Opcional: Crear todas las tablas definidas en models.py si son necesarias como base
        # para la aplicación (ej. tablas de usuarios, progreso) antes de que setup_sql de la misión
        # cree/modifique tablas específicas del juego.
        # Si setup_sql es completamente autocontenido (DROP/CREATE), esto podría no ser necesario
        # para las tablas del juego, pero sí para las tablas de la aplicación.
        # print("initialize_first_mission_db: Creando tablas base de la aplicación (si están definidas en models.py)...")
        # db.create_all() # Descomentar si tienes modelos para usuarios, etc., que deben existir.
        # print("initialize_first_mission_db: Tablas base creadas.")

        if MISSIONS:
            # Asumimos que la primera misión tiene id=1 o es la primera en la lista.
            first_mission = next((m for m in MISSIONS if m['id'] == 1), None)
            if not first_mission and MISSIONS: # Si no hay id=1, tomar la primera
                first_mission = MISSIONS[0]

            if first_mission and 'setup_sql' in first_mission:
                try:
                    print(f"initialize_first_mission_db: Ejecutando setup_sql para Misión ID: {first_mission['id']}...")
                    execute_sql_script(db.session, first_mission['setup_sql'])
                    print(f"initialize_first_mission_db: Base de datos configurada para la Misión {first_mission['id']}.")
                except Exception as e:
                    print(f"initialize_first_mission_db: Error configurando la base de datos para la primera misión: {e}")
                    # Podrías querer que la aplicación no inicie si esto falla.
            elif first_mission:
                print(f"initialize_first_mission_db: La primera misión (ID: {first_mission['id']}) no tiene 'setup_sql'. Se asume que la BD está lista o no requiere setup inicial específico para el juego.")
            else: # No first_mission
                print("initialize_first_mission_db: No se encontró la primera misión en config.py.")
        else:
            print("initialize_first_mission_db: No hay misiones definidas en config.py.")
        print("initialize_first_mission_db: Finalizado.")
