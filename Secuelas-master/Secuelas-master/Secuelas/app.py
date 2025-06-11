# Secuelas/app.py
import os
from flask import Flask
from extensions import db
from init_db import initialize_app_database # Ensures the correct function name is imported

def create_app():
    """
    Application Factory: Crea y configura la instancia de la aplicación Flask.
    """
    print("create_app: Creando instancia de Flask...")
    app_instance = Flask(__name__)
    print(f"create_app: Instancia de Flask creada con nombre '{app_instance.name}'.")

    app_instance.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'una_llave_secreta_por_defecto_muy_segura_cambiar_ya_mismo')
    
    instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)
    
    default_db_url = f"sqlite:///{os.path.join(instance_path, 'secuelas_game.db')}"
    app_instance.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', default_db_url)
    
    app_instance.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app_instance.config['SQLALCHEMY_ECHO'] = True 

    print(f"create_app: Usando DATABASE_URL: {app_instance.config['SQLALCHEMY_DATABASE_URI']}")

    print("create_app: Inicializando extensiones (SQLAlchemy) con la instancia de la app...")
    db.init_app(app_instance)
    print("create_app: SQLAlchemy inicializado.")

    from views import main_views 
    print(f"create_app: Registrando Blueprint '{main_views.name}'...")
    app_instance.register_blueprint(main_views)
    print(f"create_app: Blueprint '{main_views.name}' registrado.")

    return app_instance

if __name__ == '__main__':
    app = create_app()

    # Inicializar la base de datos: crear tablas (incluida mission_definitions)
    # y cargar misiones iniciales si es necesario.
    # This function is now correctly named initialize_app_database
    initialize_app_database(app)

    print("Ejecutando app.run()...")
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5001)))
