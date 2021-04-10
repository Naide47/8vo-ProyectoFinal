# from flask_bootstrap import Bootstrap
from flask import (Flask, g, make_response, redirect, render_template, request,
                   url_for, flash)
#from Forms import ClienteForm
from flask_wtf import CsrfProtect
from flask_wtf.csrf import CSRFProtect

import Forms
from config import DevelopmentConfig
from models import (db, empleado, pago, pedido, producto, productoTerminado,
                    proveedor, rol, usuario, venta)
import re

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


@app.route('/proveedores')
def proveedores():
    return render_template("proveedores.html")


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
