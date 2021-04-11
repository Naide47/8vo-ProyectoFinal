from flask import Flask, render_template, url_for, redirect
from flask import request
# from flask_bootstrap import Bootstrap
from flask import make_response
from flask import g,redirect
from flask_wtf import CsrfProtect
from flask_wtf.csrf import CSRFProtect
from models import db, Usuario, Empleado, Rol
from flask_security import SQLAlchemyUserDatastore
import Forms
from config import DevelopmentConfig
#from Forms import ClienteForm
from flask_wtf import CsrfProtect

csrf = CSRFProtect()
userDataStore = SQLAlchemyUserDatastore(db, Usuario, Rol)

app=Flask(__name__)
app.config.from_object(DevelopmentConfig)
# bootstrap=Bootstrap(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/ubicacion')
def ubicacion():
    return render_template("ubicacion.html")
    
@app.route('/menu')
def menu():
    return render_template("menu.html")

@app.route('/productos')
def productos():
    return render_template("productos.html")
    
@app.route('/pedidos')
def pedidos():
    return render_template("pedidos.html")

@app.route('/empleado')
def empleado_get():
    roles = db.session.query(Rol).all()
    empleados = db.session.query(Empleado).all()
    usuarios = db.session.query(Usuario).all()
    #userDataStore.get_user(empleados.id_usuario)
    #rol = db.session.query(Rol).filter(Rol.id == Usuario.rolId).all()
    return render_template("empleado.html", roles=roles, empleados=empleados, usuarios=usuarios)

@app.route('/empleado', methods=['POST'])
def empleado_post():
    if request.method == "POST":
        #datos de empleado
        nombre = request.form.get('nombreEmp')
        apellido = request.form.get('apellidoEmp')
        numeroExterior = request.form.get('NumExtEmp')
        calle = request.form.get('calleEmp')
        colonia = request.form.get('coloniaEmp')
        estatus = 1
        telefono = request.form.get('telEmp')
        fechaNacimiento = request.form.get('NacEmp')
        sueldo = request.form.get('sueldoEmp')

        nombreUsu = request.form.get('NombreUsu')
        email = request.form.get('emailUsu')
        password = request.form.get('passUsu')
        rolUsu = request.form.get('exampleRadios')
        
        #se crea un nuevo usuario
        userDataStore.create_user(
            nombre = nombreUsu,
            email = email,
            active = 1,
            password = password,
            roles = [rolUsu]  
        )
        
        db.session.commit()
        
        usuId = db.session.query(Usuario).order_by(Usuario.id.desc()).first()
        idusuario = usuId.id
        #new_usuairos_rol =  usuarios_rol(id_usuario=usuId, id_rol=rolUsu)
        #<db.session.add(new_usuairos_rol)
        
        new_empleado = Empleado(nombre = nombre, apellido = apellido, numeroExterior = numeroExterior, 
                                calle = calle, colonia = colonia, estatus = estatus, 
                                telefono = telefono, fechaNacimiento = fechaNacimiento, sueldo = sueldo, id_usuario=idusuario)
        db.session.add(new_empleado)
        db.session.commit()
    
    return redirect(url_for('empleado_get'))

@app.route('/proveedores')
def proveedores():
    return render_template("proveedores.html")

@app.route('/ventas')
def ventas():
    return render_template("ventas.html")

@app.route('/inventarioMaterial')
def inventarioMaterial():
    return render_template("inventarioMaterial.html")

@app.route('/inventarioPT')
def inventarioPT():
    return render_template("inventarioPT.html")

        
if __name__ == "__main__":
   csrf.init_app(app)
   db.init_app(app)
   with app.app_context():
     db.create_all()
      
   app.run(port=3000,debug=True)