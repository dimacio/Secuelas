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

class DocumentAccessLog(db.Model):
    __tablename__ = 'document_access_logs'
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    document_id = db.Column(db.String(50))
    access_timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    action = db.Column(db.String(50)) # e.g., 'VIEW', 'EDIT', 'CLASSIFIED_VIEW'
    remarks = db.Column(db.String(255), nullable=True)

    employee = db.relationship('Employee', backref=db.backref('access_logs', lazy=True))

    def __repr__(self):
        return f'<Log {self.log_id} by Employee {self.employee_id} on Doc {self.document_id}>'
    

# ... tus clases Archive TEST ...
class Archive(db.Model):
    __tablename__ = 'archive'
    archive_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    document_id = db.Column(db.String(50), db.ForeignKey('document_access_logs.document_id'))
    department = db.Column(db.String(50)) #,db.ForeingKey("employees.department")
    content = db.Column(db.String(255), nullable=True)

    # NO ENTIENDO PARA QUE SIRVE ESTA LINEA employee = db.relationship('Employee', backref=db.backref('access_logs', lazy=True))

    def __repr__(self):
        return f'<ID {self.archive_id}  Doc {self.document_id}>'