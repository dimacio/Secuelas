# Secuelas/app.py
import os
from flask import Flask
from extensions import db
from init_db import initialize_first_mission_db # Cambiado de initialize_database

def create_app():
    """
    Application Factory: Crea y configura la instancia de la aplicación Flask.
    """
    print("create_app: Creando instancia de Flask...")
    app_instance = Flask(__name__)
    print(f"create_app: Instancia de Flask creada con nombre '{app_instance.name}'.")

    # Configuración de la aplicación
    app_instance.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'una_llave_secreta_por_defecto_muy_segura_cambiar')
    
    # URI de la base de datos: usa variable de entorno o un valor por defecto (SQLite en memoria)
    # Para PostgreSQL, sería algo como: 'postgresql://user:password@host:port/database_name'
    app_instance.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///:memory:')
    app_instance.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app_instance.config['SQLALCHEMY_ECHO'] = True # Útil para depurar SQL generado

    print(f"create_app: Usando DATABASE_URL: {app_instance.config['SQLALCHEMY_DATABASE_URI']}")

    print("create_app: Inicializando extensiones (SQLAlchemy) con la instancia de la app...")
    db.init_app(app_instance)
    print("create_app: SQLAlchemy inicializado.")

    # Importar y registrar el Blueprint desde views.py
    # Mover la importación aquí para evitar importaciones circulares si views.py importa 'current_app'
    from views import main_views 
    print(f"create_app: Registrando Blueprint '{main_views.name}'...")
    app_instance.register_blueprint(main_views)
    print(f"create_app: Blueprint '{main_views.name}' registrado.")

    return app_instance

# El punto de entrada principal de la aplicación
if __name__ == '__main__':
    app = create_app() # Crea la aplicación usando la factory

    # Inicializar la base de datos con la aplicación creada
    # Esto asegura que las tablas (si las hay definidas en models.py para la app)
    # y el setup_sql de la primera misión se ejecuten.
    initialize_first_mission_db(app)

    print("Ejecutando app.run()...")
    # debug=True activa el reiniciador automático y el depurador.
    # host='0.0.0.0' para que sea accesible desde fuera del contenedor/máquina.
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5001)))
