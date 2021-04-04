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