# Secuelas/models.py
from extensions import db
import datetime
import json # Para serializar/deserializar las opciones de evaluación

# Modelos base de la aplicación (si los tuvieras para usuarios, etc.)
# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     # ... otros campos

class MissionDefinitionDB(db.Model):
    __tablename__ = 'mission_definitions'
    id = db.Column(db.Integer, primary_key=True) # El ID de la misión, debe ser único.
    title = db.Column(db.String(255), nullable=False)
    coordinator_message_subject = db.Column(db.Text, nullable=False)
    coordinator_message_body = db.Column(db.Text, nullable=False)
    
    # setup_sql se almacenará como un bloque de texto.
    # La aplicación lo dividirá en sentencias individuales al ejecutarlo.
    setup_sql_script = db.Column(db.Text, nullable=False)
    
    correct_query_script = db.Column(db.Text, nullable=False)
    
    # Las opciones de evaluación se guardarán como una cadena JSON.
    evaluation_options_json = db.Column(db.Text, nullable=False) 
    
    hint = db.Column(db.Text, nullable=True)
    success_message = db.Column(db.Text, nullable=False)
    
    # Campos adicionales que podrían ser útiles
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    @property
    def setup_sql(self):
        # Devuelve setup_sql_script como una lista de sentencias.
        # Asume que las sentencias están separadas por ';' o son líneas individuales.
        if not self.setup_sql_script:
            return []
        # Una lógica simple de división, podría necesitar ser más robusta
        # si las sentencias SQL contienen ';' dentro de strings.
        statements = [s.strip() for s in self.setup_sql_script.split(';') if s.strip()]
        if not statements and self.setup_sql_script.strip(): # Si no hay ; pero hay contenido
            statements = [s.strip() for s in self.setup_sql_script.splitlines() if s.strip()]
        return statements

    @property
    def evaluation_options(self):
        # Deserializa las opciones de evaluación desde JSON.
        try:
            return json.loads(self.evaluation_options_json)
        except (json.JSONDecodeError, TypeError):
            # Devolver un diccionario por defecto o vacío en caso de error
            return {}

    def __repr__(self):
        return f'<MissionDefinitionDB {self.id}: {self.title}>'

# Los modelos Employee, Document, DocumentAccessLog que tenías antes
# probablemente no sean necesarios aquí si cada misión define sus propias tablas
# a través de setup_sql. Si son para una estructura base de la aplicación,
# mantenlos, pero asegúrate de que no colisionen con las tablas de las misiones.
# Por simplicidad, los comentaré si no son esenciales para la persistencia de misiones.


