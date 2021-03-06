import datetime
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore

db = SQLAlchemy()
#Tabla que une la relación mucho a mucho de producto y productoTerminado
producto_T = db.Table('producto_T',
                      db.Column('id_producto', db.Integer, db.ForeignKey('producto.id')),
                      db.Column('id_productoTerminado', db.Integer, db.ForeignKey('productoTerminado.id')))

#Tabla que une a usuario y rol
usuarios_rol = db.Table('usuarios_rol',
                      db.Column('id_usuario', db.Integer, db.ForeignKey('usuario.id')),
                      db.Column('id_rol', db.Integer, db.ForeignKey('rol.id')))

'''
class usuarios_rol(db.Model):
    __tablename__ = 'usuarios_rol'
    id_usuario = db.Column('id_usuario', db.Integer, db.ForeignKey('usuario.id'))
    id_rol = db.Column('id_rol', db.Integer, db.ForeignKey('rol.id'))
'''

class Rol(RoleMixin, db.Model):
    __tablename__ = 'rol'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(50))
    
class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.Text)  
    active = db.Column(db.Integer)
    fecha = db.Column(db.Date, default=date.today())
    roles = db.relationship('Rol',
                          secondary=usuarios_rol,
                          backref=db.backref('usuarios', lazy='dynamic'))
    
class Empleado(db.Model):
    __tablename__ = 'empleado'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    apellido = db.Column(db.String(50))
    numeroExterior = db.Column(db.String(10))
    calle = db.Column(db.String(50))
    colonia = db.Column(db.String(50))
    estatus = db.Column(db.Integer)
    telefono = db.Column(db.String(20))
    fechaNacimiento = db.Column(db.Date)
    fechaRegistro = db.Column(db.Date, default=datetime.date.today())
    sueldo = db.Column(db.Float)
    id_usuario = db.Column('id_usuario', db.Integer,
                           db.ForeignKey('usuario.id'))

class producto(db.Model):
    tablename = 'producto'
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Float)
    descripcion = db.Column(db.String(250))
    unidadMedida = db.Column(db.String(2))
    monto = db.Column(db.Float)
    precio = db.Column(db.Float)
    fecha_registro = db.Column(db.Date, default=datetime.date.today())
    estatus = db.Column(db.Integer)
    id_pedido = db.Column('id_pedido', db.Integer, db.ForeignKey('pedido.id'))


class productoTerminado(db.Model):
    __tablename__ = 'productoTerminado'
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float)
    estatus = db.Column(db.Integer)
    fecha_registro = db.Column(db.Date, default=datetime.date.today())
    descripcion = db.Column(db.String(255))
    relacion = db.relationship('producto',
                               secondary=producto_T)


class pago(db.Model):
    __tablename__ = 'pago'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))

class venta(db.Model):
    __tablename__ = 'venta'
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Float)

    descripcion = db.Column('descripcion', db.Integer, db.ForeignKey('productoTerminado.id'))
    
    numeroExterior = db.Column(db.String(20))
    calle = db.Column(db.String(50))
    colonia = db.Column(db.String(50))
    fechaVenta = db.Column(db.DateTime, default=datetime.date.today())
    total = db.Column(db.Float)
    estatus = db.Column(db.Integer)
    id_empleado = db.Column('id_empleado', db.Integer, db.ForeignKey('empleado.id'))
    id_pago = db.Column('id_pago', db.Integer, db.ForeignKey('pago.id'))  
    
class proveedor(db.Model):
    __tablename__ = 'proveedor'
    id = db.Column(db.Integer, primary_key=True)
    empresa = db.Column(db.String(100))
    contacto = db.Column(db.String(200))
    calle = db.Column(db.String(50))
    colonia = db.Column(db.String(50))
    municipio = db.Column(db.String(60))
    estado = db.Column(db.String(60))
    telefono = db.Column(db.String(20))
    estatus = db.Column(db.Integer)    
    
class pedido(db.Model):
    tablename = 'pedido'
    id = db.Column(db.Integer, primary_key=True)
    unidadMedida = db.Column(db.String(2))
    cantidad = db.Column(db.Float)
    precio = db.Column(db.Float)
    fecha = db.Column(db.DateTime, default=datetime.date.today())
    producto = db.Column(db.String(255))
    estatus = db.Column(db.Integer)
    id_pago = db.Column('id_pago', db.Integer, db.ForeignKey('pago.id'))
    id_proveedor = db.Column('id_proveedor', db.Integer, db.ForeignKey('proveedor.id'))
    
