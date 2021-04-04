from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Pedido(db.Model):
    __tablename__ = 'pedido'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    direccion=db.Column(db.String(50))
    telefono=db.Column(db.String(50))
    tamanio=db.Column(db.String(50))
    numP=db.Column(db.Integer)
    ingredientes=db.Column(db.String(50))
    dia=db.Column(db.Integer)
    mes=db.Column(db.Integer)
    anio=db.Column(db.Integer)
    total=db.Column(db.Integer)