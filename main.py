from flask import Flask, render_template
from flask import request
# from flask_bootstrap import Bootstrap
from flask import make_response
from flask import g,redirect
from flask_wtf import CsrfProtect
from flask_wtf.csrf import CSRFProtect
from models import db
from models import (db, empleado, pago, pedido, producto, productoTerminado,
                    proveedor, rol, usuario, venta, producto_T)
import Forms
from config import DevelopmentConfig
#from Forms import ClienteForm
from flask_wtf import CsrfProtect

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

@app.route('/proveedores')
def proveedores():
    return render_template("proveedores.html")

@app.route('/ventas')
def ventas():
    
    return render_template("ventas.html")

@app.route('/ventas/agregar', methods=["POST", "GET"])
def ventasAgregar():

    if request.method == 'POST':
        descripcion=request.form['descripcion']
        cantidad=request.form['cantidad']     

        calle=request.form['calle']
        numeroExterior=request.form['numero']
        colonia=request.form['colonia']

        total=request.form['total']
        pago=request.form['metodoP']

        fechaVenta=datetime.now()

        estatus=int(1)

        id_empleado=request.form['idEmpleado']
        id_pago=request.form['idPago']
        id_producto_T.form['idProductoT']

    return redirect(url_for('ventas'))

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