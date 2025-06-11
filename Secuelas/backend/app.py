# Secuelas/backend/app.py
import os
from flask import Flask
from flask.cli import with_appcontext
from flask_cors import CORS

from extensions import db
from init_db import initialize_app_database
from api import main_api_blueprint

def create_app():
    """
    Application Factory: Creates and configures the Flask application instance.
    """
    print("create_app: Creating Flask app instance...")
    app_instance = Flask(__name__)

    # --- Configuration ---
    print("create_app: Configuring application...")
    # Load secret key from environment or use a default (change in production)
    app_instance.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'a_very_secret_default_key_that_must_be_changed')

    # Configure database path inside the 'instance' folder
    instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
    os.makedirs(instance_path, exist_ok=True)
    
    default_db_url = f"sqlite:///{os.path.join(instance_path, 'secuelas_game.db')}"
    app_instance.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', default_db_url)
    app_instance.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    print(f"create_app: Using DATABASE_URL: {app_instance.config['SQLALCHEMY_DATABASE_URI']}")

    # --- Initialize Extensions ---
    print("create_app: Initializing extensions (CORS, SQLAlchemy)...")
    CORS(app_instance, supports_credentials=True)
    db.init_app(app_instance)
    print("create_app: Extensions initialized.")

    # --- Register Blueprints ---
    print(f"create_app: Registering Blueprint '{main_api_blueprint.name}'...")
    app_instance.register_blueprint(main_api_blueprint, url_prefix='/api')
    print(f"create_app: Blueprint registered at /api.")

    # --- Register CLI Commands ---
    # This is the correct way to add custom commands to a Flask app factory.
    # The command will be aware of the application context.
    @app_instance.cli.command('init-db')
    @with_appcontext
    def init_db_command():
        """
        Clears existing data from the database and creates new tables 
        based on the defined models.
        """
        initialize_app_database(app_instance)
        print("Database has been successfully initialized.")

    print("create_app: 'init-db' command registered.")
    
    return app_instance

# --- Main Application Entry Point ---
# The app instance is created here, making it importable for WSGI servers like Gunicorn
app = create_app()

if __name__ == '__main__':
    # This block now only runs the development server when the script is executed directly.
    # The 'flask run' command in docker-compose.yml will use the 'app' object above.
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5001)))
