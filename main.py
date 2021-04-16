
import re
import traceback
from datetime import date, datetime

from flask import (Flask, flash, g, make_response, redirect, render_template,
                   request, url_for)
from flask_security import Security, SQLAlchemyUserDatastore, login_required, roles_accepted, current_user
from flask_security.utils import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security.decorators import roles_accepted, roles_required
from flask_wtf import CsrfProtect
from flask_wtf.csrf import CSRFProtect
import Forms
from config import DevelopmentConfig
from models import (Empleado, Rol, Usuario, db, pago, pedido, producto,
                    producto_T, productoTerminado, proveedor, usuarios_rol,
                    venta)

csrf = CSRFProtect()
userDataStore = SQLAlchemyUserDatastore(db, Usuario, Rol)

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)


precios = {
    'Alitas (6 piezas)': 50,
    'Papas fritas (300g)': 35,
    'Alitas (12 piezas)': 90,
    'Alitas (6 piezas) y papas (300g)': 70,
    'Alitas (6 piezas) y nuggets (4 piezas)': 75,
    'Big Wins (6 piezas)': 65,
    'Boneless (6 piezas)': 75
}

cantidades = {
    'Alitas (6 piezas)': 1.50,
    'Papas fritas (300g)': 0.3,
    'Alitas (12 piezas)': 3,
    'Alitas (6 piezas) y papas (300g)': 1.50,
    'Alitas (6 piezas) y nuggets (4 piezas)': 1.50,
    'Big Wins (6 piezas)': 2.7,
    'Boneless (6 piezas)': 1.8
}

platillos = {
    'Alitas (6 piezas)': 'ALITAS DE POLLO',
    'Papas fritas (300g)': 'PAPAS FRITAS',
    'Alitas (12 piezas)': 'ALITAS DE POLLO',
    'Alitas (6 piezas) y papas (300g)': 'ALITAS DE POLLO',
    'Alitas (6 piezas) y nuggets (4 piezas)': 'ALITAS DE POLLO',
    'Big Wins (6 piezas)': 'BIG WINS',
    'Boneless (6 piezas)': 'BONELESS'
}

objetos = []

security = Security(app, userDataStore)

@app.before_first_request
def before_first_request():
    
    if len(Rol.query.all()) != 3:
        rol = userDataStore.create_role(
            name="adm",
            description="Administrador"
        )
        rol = userDataStore.create_role(
            name="gen",
            description="Gerente"
        )
        rol = userDataStore.create_role(
            name="emp",
            description="Empleado"
        )
        
        db.session.add(rol)
        db.session.commit()
    
    if len(pago.query.all()) != 2:
        pago1 = pago(
            tipo = 'Credito'
        )
        
        db.session.add(pago1)
        db.session.commit()
        
        pago2 = pago(
            tipo = 'Efectivo'
        )
        
        db.session.add(pago2)
        db.session.commit()
        
    if not Usuario.query.filter_by(email='cruzito@email.com').first():
        userDataStore.create_user(
            nombre='Cruz Isaac',
            email='cruzito@email.com',
            active=1,
            password=generate_password_hash('cruz', method='sha256'),
            roles=['adm']
        )
        
        db.session.commit()
        
        usuario = Usuario.query.filter_by(id=1).first()
        
        cruz = Empleado(
            nombre='Cruz',
            apellido='Aranda',
            numeroExterior='111',
            calle='Calle Real',
            colonia='Colonia Real',
            estatus = 1,
            telefono = '477 1234567',
            fechaNacimiento = '2000/01/01',
            sueldo='500',
            id_usuario=usuario.id
        )
        
        db.session.add(cruz)
        db.session.commit()

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

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/validar')
@roles_accepted('adm')
def validar():
    if current_user.has_role('adm'):
        adm = True
        return render_template("empleado.html", name=current_user.nombre, adm=adm)

@app.route('/iniciarSesion', methods=['POST'])
def iniciarSesion():
    email = request.form.get('correoLogin')
    password = request.form.get('passLogin')
    remember = True if request.form.get('form1Example3') else False
    
    print(email)
    print(password)
    
    usuario = Usuario.query.filter_by(email=email).first()
    
    if not usuario or not check_password_hash(usuario.password, password):
        return redirect(url_for('index'))
    
    login_user(usuario, remember=remember)
    if current_user.has_role('adm'):
        adm = True
        return redirect(url_for('empleado_get', name=current_user.nombre, adm=adm))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/ubicacion')
def ubicacion():
    return render_template("ubicacion.html")


@app.route('/menu')
def menu():
    return render_template("menu.html")


@app.route('/pedidos')
def pedidos():
    pedidos = db.session.execute("SELECT p.*,pa.tipo,pr.empresa FROM pedido AS p INNER JOIN pago AS pa ON p.id_pago=pa.id INNER JOIN proveedor AS pr ON p.id_proveedor=pr.id WHERE p.estatus=1 ORDER BY p.id;")
    pagos=db.session.query(pago).all()
    proveedores=db.session.query(proveedor).all()
    db.session.commit()
    
    return render_template("pedidos.html", pedido=pedidos, pago=pagos, proveedor=proveedores)

@app.route('/pedidos/agregar', methods=["POST", "GET"])
def pedidosAgregar():
    #resultado = formulario_sanitizado(request.form)
    #if resultado:
    if request.method == 'POST' and request.form.get("checkM"):
        unidadMedida=request.form['checkM']
        cantidad=request.form['cantidad']
        precio=request.form['precio']
        producto=request.form['producto']
        pago=request.form['metodoP']
        fecha=datetime.now()
        empresa=request.form['empresa']
        estatus=int(1)
        
        pe=pedido(
            unidadMedida = unidadMedida,
            cantidad = cantidad,
            precio = precio,
            fecha = fecha,
            producto = producto,
            estatus = estatus,
            id_proveedor = empresa,
            id_pago = pago
        )
        flash(u'Pedido agregado con exito.', "success")
        db.session.add(pe)
        db.session.commit()
    #else:
        #flash(u'Error al agregar el pedido.', "danger")
        
    return redirect(url_for('pedidos'))


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
    rolesInac = db.session.query(Rol).all()
    empleadosInac = db.session.query(Empleado).filter(Empleado.estatus == 0).all()
    usuariosInac = db.session.query(Usuario).filter(Usuario.active == 0).all()
    us_rolesInac = db.session.query(usuarios_rol).all()
    
    #userDataStore.get_user(empleados.id_usuario)
    #rol = db.session.query(Rol).filter(Rol.id == Usuario.rolId).all()
    return render_template("empleado.html", rolesInac=rolesInac, empleadosInac=empleadosInac, usuariosInac=usuariosInac, us_rolesInac=us_rolesInac)

@app.route('/empleado/Inactivos', methods=['POST'])
def empleado_activar():
    if request.method == "POST":
        idEmpleado = request.form.get('activarE')
        empleado = db.session.query(Empleado).filter(idEmpleado == Empleado.id).first()
        #idUsuario = db.session.query(Empleado).filter(idEmpleado == Empleado.id_usuario).first()
        usuario = db.session.query(Usuario).filter(empleado.id_usuario == Usuario.id).first()

        empleado.estatus = 1
        
        db.session.add(empleado)
        db.session.commit()
    
        userDataStore.activate_user(usuario)
        db.session.commit()
    
    return redirect(url_for('empleado_get'))

@app.route('/empleado', methods=['POST'])
def empleado_post():
    resultado = formulario_sanitizado(request.form)
    if resultado:
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
                password = generate_password_hash(password, method='sha256'),
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
            
            flash(u'Operación realizada con exito.', u'success')
        
    else:
        flash(
            u'Operación fallida. Por favor, ingrese solo caracteres alfanumericos', "danger")
    
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
    #print(idEmpleado)
    empleadoM = db.session.query(Empleado).filter(idEmpleado == Empleado.id).first()
    #print(empleadoM.id_usuario)
    usuarioM = db.session.query(Usuario).filter(Usuario.id == empleadoM.id_usuario).first()
    
    #beforeRol = ""
    for ur in us_roles:
        for r in roles:
            if usuarioM.id == ur.id_usuario:
                if r.id == ur.id_rol:
                    beforeRol = r.name  
      
    return render_template("empleado.html", beforeRol=beforeRol, empleadoM=empleadoM, usuarioM=usuarioM, roles=roles, empleados=empleados, usuarios=usuarios, us_roles=us_roles)
    
@app.route('/empleado/modificarr', methods=['POST'])
def empleado_modificar_post():
    idEmp = request.form.get('idEmpM')
    idUsu = request.form.get('idUsuM')
    empleado = db.session.query(Empleado).filter(Empleado.id == idEmp).first()
    usuario = db.session.query(Usuario).filter(Usuario.id == idUsu).first()
    
    
    #datos del empleado
    empleado.nombre = request.form.get('nombreEmpM')
    empleado.apellido = request.form.get('apellidoEmpM')
    empleado.numeroExterior = request.form.get('NumExtEmpM')
    empleado.calle = request.form.get('calleEmpM')
    empleado.colonia = request.form.get('coloniaEmpM')
    empleado.telefono = request.form.get('telEmpM')
    empleado.fechaNacimiento = request.form.get('NacEmpM')
    empleado.sueldo = request.form.get('sueldoEmpM')
    
    #datos del usuario
    nombreUsu = request.form.get('NombreUsuM')
    email = request.form.get('emailUsuM')
    rolUsu = request.form.get('exampleRadiosM')
    
    rol = db.session.query(Rol).all()
    us_rol = db.session.query(usuarios_rol).all()
    
    #beforeRol = ""
    for ur in us_rol:
        for r in rol:
            if usuario.id == ur.id_usuario:
                if r.id == ur.id_rol:
                    #userDataStore.remove_role_from_user(usuario, 'adm')
                    beforeRol = r.name
                    #print(r.name)
    
    usuario.nombre = nombreUsu
    usuario.email = email
    
    if beforeRol != rolUsu:
        userDataStore.remove_role_from_user(usuario, beforeRol)
        userDataStore.add_role_to_user(usuario, rolUsu)
    
    db.session.add(usuario)
    db.session.commit()
    
    db.session.add(empleado)
    db.session.commit()
    
    return redirect(url_for('empleado_get'))
    


@app.route('/proveedores', methods=['POST', 'GET'])
# @roles_required('admin')
def proveedores():
    # form=ProveedorForm(request.form)
    getAllPro = db.session.query(proveedor).filter(
        proveedor.estatus == 1).all()
    proveDatos = ''
    if request.form.get("updateProveedores") and request.method == 'POST':
        idP = request.form['updateProveedores']
        prove = db.session.query(proveedor).filter(proveedor.id == idP).first()
        proveDatos = prove
        # print(prove)
        # print(getAllPro)
        # return render_template("proveedores.html",form=form,proveedores=getAllPro,prove=prove)
    if proveDatos:
        # return render_template("proveedores.html",form=form,proveedores=getAllPro,prove=proveDatos)
        return render_template("proveedores.html", proveedores=getAllPro, prove=proveDatos)
    else:
        # return render_template("proveedores.html",form=form,proveedores=getAllPro)
        return render_template("proveedores.html", proveedores=getAllPro)


@app.route("/proveedores/eliminar", methods=["GET", "POST"])
def eliminar():
    if request.form.get("deleteProveedores") and request.method == 'POST':
        idP = request.form['deleteProveedores']
        prov = db.session.query(proveedor).filter(proveedor.id == idP).first()
        prov.estatus = 0
        db.session.add(prov)
        db.session.commit()
        flash('Proveedor elimnado', 'danger')

    return redirect(url_for('proveedores', flash=flash))


@app.route("/proveedores/update", methods=["POST", "GET"])
def updateProv():
    if request.form.get("upProvedor") and request.method == 'POST':
        empresa = request.form['upNombreE']
        calle = request.form['upCalleE']
        contacto = request.form['upContactoE']
        colonia = request.form['upColoniaE']
        municipio = request.form['upMuniE']
        estado = request.form['upEstadoE']
        telefono = request.form['upTelE']
        idP = request.form['upProvedor']
        # result1=comprobar_sanitizado(empresa)
        # result2=comprobar_sanitizado(contacto)
        # result3=comprobar_sanitizado(calle)
        # result4=comprobar_sanitizado(colonia)
        # result5=comprobar_sanitizado(municipio)
        # result6=comprobar_sanitizado(estado)
        # result7=comprobar_sanitizado(telefono)
        # result8=comprobar_sanitizado(idP)
        # if result1 and result2 and result3 and result4 and result5 and result6 and result7 and result8:
        prov = db.session.query(proveedor).filter(proveedor.id == idP).first()
        prov.empresa = empresa
        prov.contacto = contacto
        prov.calle = calle
        prov.colonia = colonia
        prov.municipio = municipio
        prov.estado = estado
        prov.telefono = telefono
        db.session.add(prov)
        db.session.commit()
        flash('Proveedor modificado con exito', "success")
        # else:
        #flash('Operación fallida , ingrese caracteres alfanumeros',"danger")
    return redirect(url_for('proveedores'))


@app.route("/proveedores/agregar", methods=["POST", "GET"])
def addProv():
    if request.method == 'POST' and request.form.get("txtNombreE"):
        empresa = request.form['txtNombreE']
        calle = request.form['txtCalleE']
        contacto = request.form['txtContactoE']
        colonia = request.form['txtColoniaE']
        municipio = request.form['txtMunicipioE']
        estado = request.form['txtEstadoE']
        telefono = request.form['txtTelE']
        # result1=comprobar_sanitizado(empresa)
        # result2=comprobar_sanitizado(contacto)
        # result3=comprobar_sanitizado(calle)
        # result4=comprobar_sanitizado(colonia)
        # result5=comprobar_sanitizado(municipio)
        # result6=comprobar_sanitizado(estado)
        # result7=comprobar_sanitizado(telefono)
        # if result1 and result2 and result3 and result4 and result5 and result6 and result7:
        estatus = int(1)
        prov = proveedor(
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
        # else:
        #flash('Operación fallida , ingrese caracteres alfanumeros',"danger")
    return redirect(url_for('proveedores'))


@app.route('/proveedoresInactivos', methods=['POST', 'GET'])
# @roles_required('admin')
def proveedoresInactivos():
    # form=ProveedorForm(request.form)
    getAllProIna = db.session.query(proveedor).filter(
        proveedor.estatus == 0).all()
    proveDatos = ''
    if request.form.get("activarProvee") and request.method == 'POST':
        idP = request.form['activarProvee']
        prov = db.session.query(proveedor).filter(proveedor.id == idP).first()
        prov.estatus = 1

        db.session.add(prov)
        db.session.commit()
        flash('Proveedor activado con exito', "success")
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
        user = db.session.query(Usuario).filter_by(Usuario.email==email).first()

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


@app.route('/materiales')
def materiales():
    materiales = producto.query.filter_by(estatus=1).all()
    pedidos = pedido.query.all()
    return render_template("inventarioMaterial.html", materiales=materiales, pedidos=pedidos)

@app.route('/materiales/inactivos')
def materiales_inactivos():
    materiales = producto.query.filter_by(estatus=0).all()
    # pedidos = pedido.query.all()
    return render_template("inventarioMaterial.html", materiales=materiales)

@app.route('/materiales/agregar', methods=['POST'])
def materiales_agregar():
    resultado = formulario_sanitizado(request.form)
    if resultado:
        pedidoID = request.form.get('agregarPedido')
        informacion = pedido.query.filter_by(id=pedidoID).first()

        material = producto(
            cantidad=informacion.cantidad,
            descripcion=informacion.producto,
            unidadMedida=informacion.unidadMedida,
            monto=informacion.precio,
            precio=(informacion.precio * 1.33),
            id_pedido=pedidoID,
            estatus=1
        )

        db.session.add(material)
        db.session.commit()

        flash(u'Operación exitosa.', "success")

    else:
        flash(
            u'Operación fallida. Por favor, ingrese solo caracters alfanumericos', "danger")

    return redirect(url_for('materiales'))


@app.route('/materiales/modificar', methods=['POST'])
def materiales_modificar():
    resultado = formulario_sanitizado(request.form)
    if resultado:
        idMaterial = request.form.get('id-material')
        material_og = db.session.query(producto).filter(
            producto.id == idMaterial).first()

        material_og.descripcion = request.form.get('modificarDescripcion')
        material_og.unidadMedida = request.form.get('editarUM')
        material_og.cantidad = request.form.get('editarCantidad')
        material_og.monto = request.form.get('editarMonto')
        material_og.precio = request.form.get('editarPrecio')

        db.session.add(material_og)
        db.session.commit()

        flash(u'Operación exitosa.', "success")
    else:
        flash(
            u'Operación fallida. Por favor, ingrese solo caracters alfanumericos', "danger")

    return redirect(url_for('materiales'))


@app.route('/materiales/modificar_get', methods=['POST'])
def materiales_modificar_get():
    idMaterial = request.form.get('id-material-modificar')
    materiales = producto.query.filter(producto.estatus == 1)
    material_editar = producto.query.filter(producto.id == idMaterial).first()

    # return redirect(url_for('materiales'))
    return render_template("inventarioMaterial.html", material_editar=material_editar, materiales=materiales)


@app.route('/materiales/eliminar', methods=['POST'])
def materiales_eliminar():
    try:
        idMaterial = request.form.get('id-material')
        material_og = db.session.query(producto).filter(
            producto.id == idMaterial).first()

        material_og.estatus = 0
        db.session.add(material_og)
        db.session.commit()
        flash(u'Operación exitosa.', "success")
    except:
        flash(
            u'Operación fallida.', "danger")

    return redirect(url_for('materiales'))


@app.route('/materiales/eliminar_get', methods=['POST'])
def materiales_eliminar_get():
    idMaterial = request.form.get('id-material-eliminar')
    materiales = producto.query.filter(producto.estatus == 1)
    pedidos = pedido.query.all()
    return render_template("inventarioMaterial.html", materiales=materiales, idMaterial=idMaterial, pedidos=pedidos)


@app.route('/productos')
def productos():
    productos = productoTerminado.query.filter(productoTerminado.fecha_registro==date.today(), productoTerminado.estatus==1).all()
    return render_template("inventarioPT.html", productos=productos)

@app.route('/producto/inactivos')
def productos_inactivos():
    productos = productoTerminado.query.filter_by(estatus=0).all()
    return render_template("inventarioPT.html", productos=productos, inactivos=True)


@app.route('/productos/agregar', methods=['POST'])
def productos_agregar():
    resultado = formulario_sanitizado(request.form)
    if resultado:
        platillo = request.form.get('agregarPlatillo')
        complementos = request.form.getlist('agregarSalsaComplemento')
        
        descripcion = ''
        
        total = precios.get(platillo, 0)
        
        if len(complementos) > 2:
            flash(u'Operación fallida. Solo se admiten un maximo de 2 (dos) complementos', "danger")
            return redirect(url_for('productos'))
        elif platillo == 'Papas fritas (300g)' and len(complementos) != 0:
            flash(u'Operación fallida. El producto "Papas fritas (300g)" no puede tener complementos.', "danger")
            return redirect(url_for('productos'))
        elif platillo != 'Papas fritas (300g)' and len(complementos) == 0:
            flash(u'Operación fallida. Por favor, seleccione al menos un complemento.', "danger")
            return redirect(url_for('productos'))
        elif platillo == 'Papas fritas (300g)' and len(complementos) == 0:
            descripcion = platillo
        elif platillo != 'Papas fritas (300g)' and (len(complementos) >= 1 and len(complementos) <= 2):
            descripcion = platillo + ((' con salsa ' + complementos[0]) if complementos[0] != 'Takis' else ' con Takis')
            if len(complementos) == 2:
                descripcion = platillo + ' mitad ' + complementos[0] + ', mitad ' + complementos[1]
                
            if complementos[0] == 'Habanero Mango' or complementos[0] == 'Takis' :
                total += 5
            if len(complementos) == 2:    
                if complementos[1] == 'Habanero Mango' or complementos[1] == 'Takis' :
                    total += 5
        else:
            flash(u'Error de capa 8', 'info')
            return redirect(url_for('productos'))

        productoPrincipal = platillos.get(platillo)
        
        try:
            db.session.begin()
            
            producto_auxiliar = db.session.execute('SELECT * FROM producto WHERE descripcion = "{}";'.format(productoPrincipal)).first()
            productoID = producto_auxiliar.id
            
            producto_auxiliar = producto.query.filter_by(id=productoID).first()
            
            material_restar = cantidades.get(platillo)
            producto_auxiliar.cantidad -= material_restar
            
            if producto_auxiliar.cantidad < 0:
                flash(u'No hay suficientes ingredientes para el platillo principal ({})'.format(productoPrincipal), 'danger')
                return redirect(url_for('productos'))
            else:
                objetos.append(producto_auxiliar)
                
            solidos = 1
            liquidos = .1
            
            for complemento in complementos:
                resultado = False
                
                if 'BBQ' in complemento:
                    resultado = restarMateriales('SALSA BBQ', .1)
                elif 'Habanero' in complemento:
                    resultado = restarMateriales('CHILE HABANERO', 3)
                elif 'Mango' in complemento:
                    resultado = restarMateriales('MANGOS', solidos)
                elif complemento == 'Takis':
                    resultado = restarMateriales('BOLSAS DE TAKIS', solidos)
                    
                if resultado == False:
                    db.session.rollback()
                    db.session.close()
                    return redirect(url_for('productos'))
                
            if 'y nuggets' in platillo:
                if not restarMateriales('NUGGETS', .80):
                    db.session.rollback()
                    db.session.close()
                    return redirect(url_for('productos'))
            elif 'y papas' in platillo:
                if not restarMateriales('PAPAS FRITAS', .80):
                    db.session.rollback()
                    db.session.close()
                    return redirect(url_for('productos'))
                
            if not restarMateriales('PEPINOS', solidos):
                db.session.rollback()
                db.session.close()
                return redirect(url_for('productos'))
            
            if not restarMateriales('ZANAHORIAS', solidos):
                db.session.rollback()
                db.session.close()
                return redirect(url_for('productos'))
            
            if not restarMateriales('ADEREZO', liquidos):
                db.session.rollback()
                db.session.close()
                return redirect(url_for('productos'))
            
            if not restarMateriales('CAPSU', liquidos):
                db.session.rollback()
                db.session.close()
                return redirect(url_for('productos'))
            
            producto_final = productoTerminado(
                descripcion = descripcion,
                total = total,
                estatus = 1
            )

            db.session.add_all(objetos)
            db.session.commit()
            
            producto_final.relacion.append(producto_auxiliar)
            db.session.add(producto_final)
            db.session.commit()
            db.session.close()
            
            flash(u'Operación realizada con exito.', 'success')
        except Exception:
            db.session.rollback()
            db.session.close()
            traceback.print_exc()
            flash(u'Excepcion encontrada. Rollback.', 'danger')
            return redirect(url_for('productos'))
    else:
        flash(
            u'Operación fallida. Por favor, ingrese solo caracters alfanumericos', "danger")

    return redirect(url_for('productos'))


@app.route('/productos/modificar', methods=['POST'])
def productos_modificar():
    resultado = formulario_sanitizado(request.form)
    if resultado:
        productoID = request.form.get('id-producto-modificar')
        platillo = request.form.get('modificarPlatillo')
        complementos = request.form.getlist('modificarSalsaComplemento')
        
        descripcion = ''
        
        total = precios.get(platillo, 0)
        
        if len(complementos) > 2:
            flash(u'Operación fallida. Solo se admiten un maximo de 2 (dos) complementos', "danger")
            return redirect(url_for('productos'))
        elif platillo == 'Papas fritas (300g)' and len(complementos) != 0:
            flash(u'Operación fallida. El producto "Papas fritas (300g)" no puede tener complementos.', "danger")
            return redirect(url_for('productos'))
        elif platillo != 'Papas fritas (300g)' and len(complementos) == 0:
            flash(u'Operación fallida. Por favor, seleccione al menos un complemento.', "danger")
            return redirect(url_for('productos'))
        elif platillo == 'Papas fritas (300g)' and len(complementos) == 0:
            descripcion = platillo
        elif platillo != 'Papas fritas (300g)' and (len(complementos) >= 1 and len(complementos) <= 2):
            descripcion = platillo + ((' con salsa ' + complementos[0]) if complementos[0] != 'Takis' else ' con Takis')
            if len(complementos) == 2:
                descripcion = platillo + ' mitad ' + complementos[0] + ', mitad ' + complementos[1]
                
            if complementos[0] == 'Habanero Mango' or complementos[0] == 'Takis' :
                total += 5
            if len(complementos) == 2:    
                if complementos[1] == 'Habanero Mango' or complementos[1] == 'Takis' :
                    total += 5
        else:
            flash(u'Error de capa 8', 'info')
            return redirect(url_for('productos'))
                
        producto_mod = productoTerminado.query.filter_by(id=productoID).first()
        producto_mod.descripcion = descripcion
        producto_mod.total = total
        
        db.session.add(producto_mod)
        db.session.commit()
        
        flash(u'Operación realizada con exito.', 'success')
        
    else:
        flash(
            u'Operación fallida. Por favor, ingrese solo caracters alfanumericos', "danger")

    return redirect(url_for('productos'))

@app.route('/productos/modificar_get', methods=['POST'])
def productos_modificar_get():
    productoID = request.form.get('id-producto-modificar')
    productoD = request.form.get('descripcion-producto-modificar')
    platillo = ''
    complemento1 = ''
    complemento2 = ''
    
    if productoD == 'Papas fritas (300g)':
        platillo = productoD
    else:    
        platillo = re.search('(.+?) con', productoD)
        if platillo:
            platillo = platillo.group(1)
            # print(platillo)
        else:
            platillo = re.search('(.+?) mitad', productoD)
            platillo = platillo.group(1)
            # print(platillo)
            
        complemento1 = re.search('con (.*)', productoD)
        complemento2 = ''
        if complemento1:
            complemento1 = complemento1.group(1)
            if 'salsa' in complemento1:
                complemento1 = re.search('salsa (.*)', complemento1)
                complemento1 = complemento1.group(1)
        else:
            complemento1 = re.search('mitad (.+?),', productoD)
            complemento2 = re.search(', mitad (.*)', productoD)
            complemento1 = complemento1.group(1)
            complemento2 = complemento2.group(1)
    
    productos = productoTerminado.query.filter(productoTerminado.fecha_registro==datetime.date.today(), productoTerminado.estatus==1).all()
    return render_template("inventarioPT.html", productos=productos, productoID=productoID, platillo=platillo, complemento1=complemento1, complemento2=complemento2)

@app.route('/productos/eliminar', methods=['POST'])
def productos_eliminar():
    resultado = formulario_sanitizado(request.form)
    if resultado:
        productoTerminadoID = request.form.get("id-producto-el")
        
        producto_aux = productoTerminado.query.filter_by(id=productoTerminadoID).first()
        
        producto_aux.estatus = 0
        
        db.session.add(producto_aux)
        db.session.commit()
        
        flash(u'Operación realizada con exito', 'success')
        
    else:
        flash(u'Operación fallida en intentar eliminar', 'danger')
    
    return redirect(url_for('productos'))

@app.route('/productos/eliminar_get', methods=['POST'])
def productos_eliminar_get():
    resultado = formulario_sanitizado(request.form)
    if resultado:
        productoTerminadoID = request.form.get("id-producto-eliminar")
        productos = productoTerminado.query.filter(productoTerminado.fecha_registro==datetime.date.today(), productoTerminado.estatus==1).all()
        return render_template("inventarioPT.html", productos=productos, productoTerminadoID=productoTerminadoID)
    else:
        flash(u'Operación fallida en intentar eliminar', 'danger')
        return redirect(url_for('productos'))

def comprobar_sanitizado(campo):

    esta_sanitizado = re.match("[a-zA-Z0-9]+", campo)

    if esta_sanitizado:
        resultado = esta_sanitizado.group(0)
    else:
        resultado = None

    return resultado


def formulario_sanitizado(formulario):

    for campo in formulario:
        if comprobar_sanitizado(formulario[campo]) == None:
            return False
        else:
            continue

    return True

def restarMateriales(aux, cantidad):
    
    material = db.session.execute('SELECT * FROM producto WHERE descripcion = "{}"'.format(aux)).first()
    materialID = material.id
    material = producto.query.filter_by(id=materialID).first()
    
    material.cantidad -= cantidad
    
    if material.cantidad < 0:
        flash(u'No hay suficientes materiales ({})'.format(aux), 'danger')
        return False
    else:
        objetos.append(material)
        return True

if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.run(port=3000, debug=True)
