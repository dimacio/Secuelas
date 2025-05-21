from extensions import db
import datetime

# ... tus clases Employee y DocumentAccessLog ...
class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True) # Siempre aclara cual es la Primary Key
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100))
    security_clearance = db.Column(db.Integer, default=1)
    hire_date = db.Column(db.Date)

    def __repr__(self):
        return f'<Employee {self.id}: {self.name}>'

# En models.py
# (Asegúrate de tener 'import datetime' al inicio del archivo si aún no está)

# ... (Employee model permanece igual) ...

class Document(db.Model):
    __tablename__ = 'documents'
    # Usaremos un ID numérico autoincremental como clave primaria interna.
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Este será el identificador textual único que usas en tus misiones (ej: 'PROYECTO_QUIMERA')
    document_token = db.Column(db.String(50), unique=True, nullable=False, index=True)
    title = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True) # Un breve resumen o descripción del documento
    classification_level = db.Column(db.Integer, default=1) # Nivel de clasificación (ej: 1=General, 5=Alto Secreto)
    # Podrías añadir quién creó el documento si es relevante:
    # created_by_employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=True)
    # creator = db.relationship('Employee', backref=db.backref('created_documents', lazy='dynamic'))
    creation_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # El backref 'access_logs' se creará desde la relación en DocumentAccessLog
    
    def __repr__(self):
        return f'<Document {self.id}: {self.document_token} - {self.title}>'

class DocumentAccessLog(db.Model):
    __tablename__ = 'document_access_logs'
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    
    # Cambiamos document_id para que sea una ForeignKey al 'document_token' de la tabla 'documents'
    # Esto asegura la integridad referencial.
    document_token_fk = db.Column(db.String(50), db.ForeignKey('documents.document_token'), nullable=False, index=True)
    
    access_timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    action = db.Column(db.String(50)) 
    remarks = db.Column(db.String(255), nullable=True)

    employee = db.relationship('Employee', backref=db.backref('access_logs', lazy=True))
    
    # Nueva relación para acceder fácilmente al objeto Document desde un log
    # Usamos foreign_keys para especificar la columna de unión ya que 'document_token_fk' es el nombre de la columna.
    document = db.relationship('Document', foreign_keys=[document_token_fk], backref=db.backref('all_access_logs', lazy='dynamic'))

    def __repr__(self):
        # Actualizamos para reflejar el cambio a document_token_fk si es necesario para la representación
        return f'<Log {self.log_id} by Employee {self.employee_id} on Doc Token {self.document_token_fk}>'

# Eliminar la clase Archive:
# class Archive(db.Model):
#     ... (todo el contenido de la clase Archive se elimina) ...