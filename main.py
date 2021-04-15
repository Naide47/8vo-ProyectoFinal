from flask import Flask, render_template,redirect,url_for,flash
from flask import request
# from flask_bootstrap import Bootstrap
from flask import make_response
from flask import g,redirect
from flask_wtf import CsrfProtect
from flask_wtf.csrf import CSRFProtect
from models import db
from models import pedido,proveedor,usuario
import Forms
from config import DevelopmentConfig
#from Forms import ClienteForm
from flask_wtf import CsrfProtect
from Forms import ProveedorForm

csrf = CSRFProtect()

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
def empleado():
    return render_template("empleado.html")

@app.route('/proveedores', methods=['POST','GET'])
#@roles_required('admin')
def proveedores():
    form=ProveedorForm(request.form)
    getAllPro=db.session.query(proveedor).filter(proveedor.estatus==1).all()
    proveDatos=''
    if request.form.get("updateProveedores") and request.method == 'POST':
        idP=request.form['updateProveedores']
        prove=db.session.query(proveedor).filter(proveedor.id==idP).first()
        proveDatos=prove
        #print(prove)
        #print(getAllPro)
        #return render_template("proveedores.html",form=form,proveedores=getAllPro,prove=prove)
    if proveDatos:
        return render_template("proveedores.html",form=form,proveedores=getAllPro,prove=proveDatos)
    else:
        return render_template("proveedores.html",form=form,proveedores=getAllPro)

@app.route("/proveedores/eliminar", methods=["GET", "POST"])
def eliminar():
    if request.form.get("deleteProveedores") and request.method =='POST':
        idP=request.form['deleteProveedores']
        prov=db.session.query(proveedor).filter(proveedor.id==idP).first()
        prov.estatus=0
        db.session.add(prov)
        db.session.commit()
        flash('Proveedor elimnado', 'danger')
        
    return redirect(url_for('proveedores',flash=flash))

@app.route("/proveedores/update" , methods=["POST","GET"])
def updateProv():
    if request.form.get("upProvedor") and request.method =='POST':
        empresa=request.form['upNombreE']
        calle=request.form['upCalleE']
        contacto=request.form['upContactoE']
        colonia=request.form['upColoniaE']
        municipio=request.form['upMuniE']
        estado=request.form['upEstadoE']
        telefono=request.form['upTelE']
        idP=request.form['upProvedor']
        #result1=comprobar_sanitizado(empresa)
        #result2=comprobar_sanitizado(contacto)
        #result3=comprobar_sanitizado(calle)
        #result4=comprobar_sanitizado(colonia)
        #result5=comprobar_sanitizado(municipio)
        #result6=comprobar_sanitizado(estado)
        #result7=comprobar_sanitizado(telefono)
        #result8=comprobar_sanitizado(idP)
        #if result1 and result2 and result3 and result4 and result5 and result6 and result7 and result8:
        prov=db.session.query(proveedor).filter(proveedor.id==idP).first()
        prov.empresa=empresa
        prov.contacto=contacto
        prov.calle=calle
        prov.colonia=colonia
        prov.municipio=municipio
        prov.estado=estado
        prov.telefono=telefono
        db.session.add(prov)
        db.session.commit()
        flash('Proveedor modificado con exito',"success")
        #else:
            #flash('Operación fallida , ingrese caracteres alfanumeros',"danger")
    return redirect(url_for('proveedores'))

@app.route("/proveedores/agregar" , methods=["POST","GET"])
def addProv():
    if  request.method == 'POST' and  request.form.get("txtNombreE"):
        empresa=request.form['txtNombreE']
        calle=request.form['txtCalleE']
        contacto=request.form['txtContactoE']
        colonia=request.form['txtColoniaE']
        municipio=request.form['txtMunicipioE']
        estado=request.form['txtEstadoE']
        telefono=request.form['txtTelE']
        #result1=comprobar_sanitizado(empresa)
        #result2=comprobar_sanitizado(contacto)
        #result3=comprobar_sanitizado(calle)
        #result4=comprobar_sanitizado(colonia)
        #result5=comprobar_sanitizado(municipio)
        #result6=comprobar_sanitizado(estado)
        #result7=comprobar_sanitizado(telefono)
        #if result1 and result2 and result3 and result4 and result5 and result6 and result7:
        estatus=int(1)
        prov=proveedor(
            empresa=empresa,
           contacto=contacto,
            calle=calle,
            colonia=colonia,
            municipio=municipio,
            estado=estado,
            telefono=telefono,
            estatus=estatus
        )
        db.session.add(prov)
        db.session.commit()
        flash('Proveedor agregado con exito', "success")
        #else:
            #flash('Operación fallida , ingrese caracteres alfanumeros',"danger")
    return redirect(url_for('proveedores'))
  
@app.route('/proveedoresInactivos', methods=['POST','GET'])
#@roles_required('admin')
def proveedoresInactivos():
    form=ProveedorForm(request.form)
    getAllProIna=db.session.query(proveedor).filter(proveedor.estatus==0).all()
    proveDatos=''
    if request.form.get("activarProvee") and request.method == 'POST':
        idP=request.form['activarProvee']
        prov=db.session.query(proveedor).filter(proveedor.id==idP).first()
        prov.estatus=1
        
        db.session.add(prov)
        db.session.commit()
        flash('Proveedor activado con exito',"success")
        return redirect(url_for("proveedores"))
    return render_template("proveedoresIna.html",proveedores=getAllProIna,)
       
@app.route("/registrar", methods=["POST","GET"])
def registrar():
    if request.method == "POST":
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        roles=request.form.get('roles')
        #Consultamos si existe un usuario ya registrado con el email.
        user = db.session.query(usuario).filter_by(usuario.email==email).first()

        if user: #El usuario existe y regresamos a la página de registro.
            flash('El correo ya existe')
            return redirect(url_for('menu'))

        #Creamos un nuevo usuario
        #newuser = User(email=email, name=name, 
        #password=generate_password_hash(password,method='sha256'))
        userDataStore.create_user(
            name=name, email=email, 
            password=generate_password_hash(password, method='sha256')
        )
        userDataStore.create_role(name='cliente', description="cliente")
        #user_rol=db.session.execute("insert into  users_roles(userID,roleID)values("+User.id+",2);")
        #Agregamos el usuario a la bd.
        db.session.commit()
        return redirect(url_for('proveedores'))
    else:
        return render_template("register.html")

@app.route('/ventas')
def ventas():
    return render_template("ventas.html")

@app.route('/inventarioMaterial')
def inventarioMaterial():
    return render_template("inventarioMaterial.html")

@app.route('/inventarioPT')
def inventarioPT():
    return render_template("inventarioPT.html")

#error 404 
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(500)
def error_server(e):
    return render_template("404.html")

def comprobar_sanitizado(campo):
    esta_sanitizado =re.match("[a-zA-Z0-9]+",campo)
    if esta_sanitizado:
        resultado=esta_sanitizado.group(0)
    else:
        resultado=None
    return resultado
def formulario_sanitizado(formulario):
    for campo in formulario:
        if comprobar_sanitizado(formulario[campo])==None:
            return False
        else:
            continue
    return True
            
        
        
if __name__ == "__main__":
   csrf.init_app(app)
   db.init_app(app)
   with app.app_context():
     db.create_all()
      
   app.run(port=3000,debug=True)