<<<<<<< HEAD
=======
from flask import Flask, render_template,redirect,url_for,flash
from flask import request
>>>>>>> f6d8163c20382ec46d757c6e7f51d2a5b84ec878
# from flask_bootstrap import Bootstrap
from flask import (Flask, g, make_response, redirect, render_template, request,
                   url_for, flash)
#from Forms import ClienteForm
from flask_wtf import CsrfProtect
from flask_wtf.csrf import CSRFProtect
<<<<<<< HEAD

import Forms
from config import DevelopmentConfig
from models import (db, empleado, pago, pedido, producto, productoTerminado,
                    proveedor, rol, usuario, venta)
import re
=======
from models import db
from models import pedido,proveedor
import Forms
from config import DevelopmentConfig
#from Forms import ClienteForm
from flask_wtf import CsrfProtect
from Forms import ProveedorForm
>>>>>>> f6d8163c20382ec46d757c6e7f51d2a5b84ec878

csrf = CSRFProtect()

app = Flask(__name__)
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
       


@app.route('/ventas')
def ventas():
    return render_template("ventas.html")


@app.route('/materiales')
def materiales():
    inventarioMaterial = producto.query.all()
    return render_template("inventarioMaterial.html", inventarioMaterial=inventarioMaterial)


@app.route('/materiales/agregar', methods=['POST'])
def materiales_agregar():
    resultado = formulario_sanitizado(request.form)
    if resultado:
        producto_agregar = producto(
            cantidad=request.form.get('agregarCantidad'),
            descripcion=request.form.get('agregarDescripcion'),
            unidadMedida=request.form.get('agregarUM'),
            monto=request.form.get('agregarMonto'),
            precio=request.form.get('agregarPrecio'),
            estatus=1
        )

        flash(u'Operación exitosa.', "success")

        db.session.add(producto_agregar)
        db.session.commit()
    else:
        flash(
            u'Operación fallida. Por favor, ingrese solo caracters alfanumericos', "danger")

    return redirect(url_for('materiales'))


@app.route('/materiales/modificar', methods=['POST'])
def materiales_modificar():
    pass

@app.route('/materiales/eliminar', methods=['POST'])
def materiales_eliminar():
    pass


@app.route('/productos')
def productos():
    return render_template("inventarioPT.html")


@app.route('/productos/agregar', methods=['POST'])
def productos_agregar():
    resultado = formulario_sanitizado(request.form)
    if resultado:
        productoTerminado_agregar = productoTerminado(
            
        )
        
        flash(u'Operación exitosa.', "success")

        db.session.add(productoTerminado_agregar)
        db.session.commit()
    else:
        flash(
            u'Operación fallida. Por favor, ingrese solo caracters alfanumericos', "danger")
        
    return redirect(url_for('productos'))


@app.route('/productos/modificar', methods=['POST'])
def productos_modificar():
    pass


@app.route('/productos/eliminar', methods=['POST'])
def productos_eliminar():
    pass


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


if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.run(port=3000, debug=True)
