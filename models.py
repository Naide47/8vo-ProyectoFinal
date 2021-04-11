import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

db = SQLAlchemy()
#Tabla que une la relación mucho a mucho de producto y productoTerminado
producto_T = db.Table('producto_T',
                      db.Column('id_producto', db.Integer, db.ForeignKey('producto.id')),
                      db.Column('id_productoTerminado', db.Integer, db.ForeignKey('productoTerminado.id')))

#Tabla que une a usuario y rol
usuarios_rol = db.Table('usuarios_rol',
                      db.Column('id_usuario', db.Integer, db.ForeignKey('usuario.id')),
                      db.Column('id_rol', db.Integer, db.ForeignKey('rol.id')))

class rol(db.Model):
    __tablename__ = 'rol'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    descripcion = db.Column(db.String(50))
    
class usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(70))  
    estatus = db.Column(db.Integer)
    fecha = db.Column(db.DateTime, default=datetime.date.today())

class empleado(db.Model):
    __tablename__ = 'empleado'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    apellido = db.Column(db.String(50))
    numeroExterior = db.Column(db.String(10))
    calle = db.Column(db.String(50))
    colonia = db.Column(db.String(50))
    estatus = db.Column(db.Integer)
    telefono = db.Column(db.String(20))
    fechaNacimiento = db.Column(db.DateTime)
    fechaRegistro = db.Column(db.DateTime, default=datetime.date.today())
    sueldo = db.Column(db.Float)
    id_usuario = db.Column('id_usuario', db.Integer, db.ForeignKey('usuario.id'))

class producto(db.Model):
    __tablename__ = 'producto'
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Float)
    descripcion = db.Column(db.String(250))
    unidadMedida = db.Column(db.Float)
    monto = db.Column(db.Float)
    precio = db.Column(db.Float)
    estatus = db.Column(db.Integer)
    
class productoTerminado(db.Model):
    __tablename__ = 'productoTerminado'
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float)
    estatus = db.Column(db.Integer)
    #descripcion = db.relationship('producto',
                                  #secondary=producto_T,
                                  #backref=db.backref('productoTerminado', lazy='dynamic'))

class pago(db.Model):
    __tablename__ = 'pago'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))

class venta(db.Model):
    __tablename__ = 'venta'
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Float)
    descripcion = db.Column(db.String(250))
    numeroExterior = db.Column(db.String(20))
    calle = db.Column(db.String(50))
    colonia = db.Column(db.String(50))
    fechaVenta = db.Column(db.DateTime, default=datetime.date.today())
    total = db.Column(db.Float)
    estatus = db.Column(db.Integer)
    id_empleado = db.Column('id_empleado', db.Integer, db.ForeignKey('empleado.id'))
    id_pago = db.Column('id_pago', db.Integer, db.ForeignKey('pago.id'))
    id_producto_T = db.Column('id_producto_T', db.Integer, db.ForeignKey('producto_T.id_productoTerminado'))    
    
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
    __tablename__ = 'pedido'
    id = db.Column(db.Integer, primary_key=True)
    unidadMedida = db.Column(db.Float)
    cantidad = db.Column(db.Float)
    precio = db.Column(db.Float)
    fecha = db.Column(db.DateTime, default=datetime.date.today())
    id_producto = db.Column('id_producto', db.Integer, db.ForeignKey('producto.id'))
    id_pago = db.Column('id_pago', db.Integer, db.ForeignKey('pago.id'))
    
class proveedor_T(db.Model):
    __tablename__ = 'proveedor_T'
    id = db.Column(db.Integer, primary_key=True)
    id_proveedor = db.Column('id_proveedor', db.Integer, db.ForeignKey('proveedor.id'))
    id_pedido = db.Column('id_pedido', db.Integer, db.ForeignKey('pedido.id'))