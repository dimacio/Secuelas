# Este archivo se crea expresamente para evitar la llamada recurrente entre app.py y models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()