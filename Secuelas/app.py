import os
from flask import Flask

from extensions import db

from init_db import initialize_database
# Función para inicializar la base de datos


def create_app():
    """
    Application Factory: Crea y configura la instancia de la aplicación Flask.
    """
    print("create_app: Creando instancia de Flask...")
    app_instance = Flask(__name__)
    print(f"create_app: Instancia de Flask creada con nombre '{app_instance.name}'.")

    # Configuración de la aplicación
    app_instance.config['SECRET_KEY'] = 'tu_super_secreta_llave_aqui_cambiala_finalmente'
    app_instance.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Base de datos en memoria para el demo
    app_instance.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    print("create_app: Inicializando extensiones (SQLAlchemy) con la instancia de la app...")
    db.init_app(app_instance) # Inicializa SQLAlchemy con la instancia de la app
    print("create_app: SQLAlchemy inicializado.")

    # Importar y registrar el Blueprint desde views.py
    from views import main_views # Importa el Blueprint
    print(f"create_app: Registrando Blueprint '{main_views.name}'...")
    app_instance.register_blueprint(main_views) # Registra el Blueprint
    print(f"create_app: Blueprint '{main_views.name}' registrado.")

    # Opcional: Código de depuración para ver las rutas registradas
    # print("*"*20 + " RUTAS REGISTRADAS en create_app " + "*"*20)
    # for rule in app_instance.url_map.iter_rules():
    #     print(f"Endpoint: {rule.endpoint}, Path: {str(rule)}")
    # print("*"*20 + " FIN RUTAS REGISTRADAS " + "*"*20)

    return app_instance

# El punto de entrada principal de la aplicación
if __name__ == '__main__':
    app = create_app() # Crea la aplicación usando la factory

    # Inicializar la base de datos con la aplicación creada
    # Esto asegura que las tablas se creen antes de que se sirvan las primeras peticiones.
    initialize_database(app)

    print("Ejecutando app.run()...")
    # debug=True activa el reiniciador automático y el depurador.
    # El patrón de factory es más robusto con el reiniciador.
    app.run(debug=True, host='0.0.0.0', port=5001)
