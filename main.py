from flask import Flask, render_template,redirect,url_for,flash
from flask import request
# from flask_bootstrap import Bootstrap
from flask import make_response
from flask import g,redirect
from flask_wtf import CsrfProtect
from flask_wtf.csrf import CSRFProtect
from models import db, Usuario, Empleado, Rol, pedido,proveedor, usuarios_rol
from flask_security import SQLAlchemyUserDatastore
import Forms
from config import DevelopmentConfig
#from Forms import ClienteForm
from flask_wtf import CsrfProtect
#from Forms import ProveedorForm

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
    empleados = db.session.query(Empleado).filter(Empleado.estatus == 1).all()
    usuarios = db.session.query(Usuario).filter(Usuario.active == 1).all()
    us_roles = db.session.query(usuarios_rol).all()
    
    #userDataStore.get_user(empleados.id_usuario)
    #rol = db.session.query(Rol).filter(Rol.id == Usuario.rolId).all()
    return render_template("empleado.html", roles=roles, empleados=empleados, usuarios=usuarios, us_roles=us_roles)

@app.route('/empleado/Inactivos')
def empleadoInac_get():
    roles = db.session.query(Rol).all()
    empleados = db.session.query(Empleado).filter(Empleado.estatus == 0).all()
    usuarios = db.session.query(Usuario).filter(Usuario.active == 0).all()
    us_roles = db.session.query(usuarios_rol).all()
    
    #userDataStore.get_user(empleados.id_usuario)
    #rol = db.session.query(Rol).filter(Rol.id == Usuario.rolId).all()
    return render_template("empleado.html", roles=roles, empleados=empleados, usuarios=usuarios, us_roles=us_roles)


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

@app.route('/eliminarEmp', methods=['POST'])
def empleado_eliminar():
    if request.method == "POST":
        idEmpleado = request.form.get('eliminarE')
        empleado = db.session.query(Empleado).filter(idEmpleado == Empleado.id).first()
        #idUsuario = db.session.query(Empleado).filter(idEmpleado == Empleado.id_usuario).first()
        usuario = db.session.query(Usuario).filter(empleado.id_usuario == Usuario.id).first()

        empleado.estatus = 0
        
        db.session.add(empleado)
        db.session.commit()
    
        userDataStore.deactivate_user(usuario)
        db.session.commit()
    
    return redirect(url_for('empleado_get'))

@app.route('/empleado/modificar', methods=['POST'])
def empleado_modificar():
    roles = db.session.query(Rol).all()
    empleados = db.session.query(Empleado).filter(Empleado.estatus == 1).all()
    usuarios = db.session.query(Usuario).filter(Usuario.active == 1).all()
    us_roles = db.session.query(usuarios_rol).all()
    
    idEmpleado = request.form.get('modificarE')
    print(idEmpleado)
    empleadoM = db.session.query(Empleado).filter(idEmpleado == Empleado.id).first()
    print(empleadoM)
    #usuario = db.session.query(Usuario).filter(empleado.id_usuario == Usuario.id).first()
      
    return render_template("empleado.html", empleadoM=empleadoM, roles=roles, empleados=empleados, usuarios=usuarios, us_roles=us_roles)
    
    '''
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
    '''
    

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