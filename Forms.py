from wtforms import Form 
from wtforms import StringField, TextField, PasswordField, IntegerField, SelectField
from wtforms import validators

class UsuarioForm(Form):
    id = IntegerField('id')
    nombre = StringField('Nombre de usuario',[
        validators.required(message='El nombre de usuario es requerido'),
        validators.length(min=3,max=50,message='Nombre de usuario no valido')
    ])
    password = PasswordField('Contraseña', [
        validators.required(message='Se requiere de una contraseña'),
        validators.length(min=3, max=10, message='La contraseña no es valida')
    ])
    rol = SelectField('Rol', choices=[
        ("1", "Admin"),
        ("2", "Gerente"),
        ("3", "Empleado")
    ])

class EmpleadoForm(Form):
    id = IntegerField('id')
    
    nombre = StringField('Nombre', [
        validators.required(message='El nombre es requerido'),
        validators.length(min=3,max=50,message='Nombre no valido')
    ])
    apellido = StringField('Apellido(s)', [
        validators.required(message='El apellido es requerido'),
        validators.length(min=3,max=100,message='Apellido no valido')
    ])
    
    direccion=StringField('Dirección',[
        validators.required(message='La dirección es requerida'),
        validators.length(min=3,max=50,message='Direccion no valida')
    ])
    telefono=StringField('Telefono',[
        validators.required(message='El telefono es requerido'),
        validators.length(min=3,max=10,message='Telefono no valida')
    ])