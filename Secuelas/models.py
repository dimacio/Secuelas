# Secuelas/models.py
from extensions import db
import datetime

# Estos modelos definen tablas que podrían ser parte de la aplicación general
# (ej. para usuarios, progreso guardado, etc.) si decides persistirlas.
# Para el juego de misiones actual, donde cada misión usa `setup_sql` para
# crear/modificar sus propias tablas de juego (employees, documents, etc.),
# estos modelos SQLAlchemy no gestionan directamente el esquema de las tablas
# *dentro* del sandbox de la misión. Sin embargo, `db.create_all()` podría
# llamarse en `init_db.py` para crear tablas persistentes de la aplicación
# (como `users`, `user_progress`) si las añades aquí.

class Employee(db.Model):
    __tablename__ = 'employees_app_base' # Renombrar para evitar colisión con tablas de misión
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # ... otros campos si esta tabla fuera para datos persistentes de la app
    # y no solo un ejemplo que las misiones recrean.

    def __repr__(self):
        return f'<EmployeeAppBase {self.id}: {self.name}>'

class Document(db.Model):
    __tablename__ = 'documents_app_base' # Renombrar
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    document_token = db.Column(db.String(50), unique=True, nullable=False, index=True)
    # ...

    def __repr__(self):
        return f'<DocumentAppBase {self.id}: {self.document_token}>'

class DocumentAccessLog(db.Model):
    __tablename__ = 'document_access_logs_app_base' # Renombrar
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # ...

    def __repr__(self):
        return f'<LogAppBase {self.log_id}>'

# --- Modelos Potenciales para Funcionalidad Extendida (Usuarios, Progreso) ---
# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     password_hash = db.Column(db.String(128)) # Almacenar hashes
#     role = db.Column(db.String(50), default='student') # student, teacher
#     # ... otros campos

# class UserProgress(db.Model):
#     __tablename__ = 'user_progress'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     mission_id = db.Column(db.Integer, nullable=False) # Podría ser un FK a una tabla de MissionDefinition
#     status = db.Column(db.String(50), default='pending') # pending, attempted, completed
#     last_attempt_query = db.Column(db.Text, nullable=True)
#     attempts = db.Column(db.Integer, default=0)
#     completed_at = db.Column(db.DateTime, nullable=True)
#     # ...

# class MissionDefinitionDB(db.Model): # Si las misiones se guardan en BD
#      __tablename__ = 'mission_definitions'
#      id = db.Column(db.Integer, primary_key=True) # El ID de la misión
#      title = db.Column(db.String(255), nullable=False)
#      coordinator_message_subject = db.Column(db.Text)
#      coordinator_message_body = db.Column(db.Text)
#      setup_sql_script = db.Column(db.Text) # El script SQL para setup
#      correct_query_script = db.Column(db.Text) # El script SQL correcto
#      evaluation_options_json = db.Column(db.Text) # Opciones de evaluación como JSON string
#      hint = db.Column(db.Text)
#      success_message = db.Column(db.Text)
#      # ... otros campos como orden, dificultad, creado_por_user_id, etc.
