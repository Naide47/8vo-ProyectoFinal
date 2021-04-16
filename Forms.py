from wtforms import Form 
from wtforms import StringField, TextField, PasswordField,RadioField,IntegerField
from wtforms import validators

class ClienteForm(Form):
    id=IntegerField('id')
    nombre=StringField('Nombre',[
        validators.required(message='El nombre es requerido'),
        validators.length(min=3,max=50,message='Nombre no valido')
    ])
    direccion=StringField('Dirección',[
        validators.required(message='La dirección es requerida'),
        validators.length(min=3,max=50,message='Direccion no valida')
    ])
    telefono=StringField('Telefono',[
        validators.required(message='El telefono es requerido'),
        validators.length(min=3,max=10,message='Telefono no valida')
    ])
    tamanio = RadioField('Tamaño pizza',
                      [validators.required(message='El tamaño  es requerido')],
                      choices=[('Chica', 'Chica $40'), ('Mediana', 'Mediana $80'), ('Grande', 'Grande $120')])
    ingredientes = RadioField('Ingredientes',
        [validators.required(message='Este campo es requerido')], 
        choices=[('Jamon', 'Jamon $10'),
                 ('Piña', 'Piña $15'),
                 ('Champiñones', 'Champiñones $20')])
    numP=IntegerField('Cantidad pizzas',[
        validators.required(message='El campo es requerido')
    ])
    dia=IntegerField('Dia', [
        validators.required(message='El campo es requerido')
    ])
    mes=IntegerField('Mes', [
        validators.required(message='El campo es requerido ')
    ])
    anio=IntegerField('Año', [
        validators.required(message='El campo es requerido ')])

class ProveedorForm(Form):
    id=IntegerField('id')
    empresa = StringField('Empresa',[
        validators.required(message='El nombre de la empresa es requerido'),
        validators.length(min=3,max=25, message="El nombre no cumple con los solicitado")
    ])
    contacto=StringField('Contacto',[
        validators.required(message='El nombre del contacto es requerido'),
        validators.length(min=3,max=25,message="El nombre del contacto no valido")
    ])
    calle=StringField('Calle',[
        validators.required(message='La calle es requerida'),
        validators.length(min=2,max=25,message="La calle no es valida")
    ])
    colonia=StringField('Colonia',[
        validators.required(message='La colonia es requerida'),
        validators.length(min=2,max=25,message="La colonia no es valida")
    ])
    Municipio=StringField('Municipio',[
        validators.required(message="El municipio es requerido"),
        validators.length(min=2,max=25,message="El municipio no es valido")
    ])
    Estado=StringField('Estado',[
        validators.required(message="El estado es requerido"),
        validators.length(min=2,max=25,message="El estado no es valido")
    ])
    Telefono=StringField('Telefono',[
        validators.required(message="El telefono es requerido"),
        validators.length(min=9,max=13,message="El telefono no es valido")
    ])