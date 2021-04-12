from flask import Flask, render_template
from flask import request
# from flask_bootstrap import Bootstrap
from flask import make_response
from flask import g,redirect
from flask_wtf import CsrfProtect
from flask_wtf.csrf import CSRFProtect
from models import db
from models import pedido
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
    pedidos = db.session.execute("select p.*,pro.descripcion,pa.tipo from pedido as p inner join producto as pro on p.id_producto=pro.id inner join pago as pa on p.id_pago=pa.id;")
    db.session.commit()
    
    return render_template("pedidos.html", pedido=pedidos)

@app.route('/pedidos/agregar', methods=["POST","GET"])
def pedidosAgregar():
    if  request.method == 'POST':
        unidadMedida=request.form['checkM']
        cantidad=request.form['cantidad']
        precio=request.form['precio']
        producto=request.form['producto']
        tipo=request.form['slT']
        
        pe=pedido(
            unidadMedida=unidadMedida,
           cantidad=cantidad,
            precio=precio,
            id_producto=producto,
            id_pago=tipo)
        
        db.session.add(pe)
        db.session.commit()
    
    return render_template("pedidos.html", pe=pedido)

@app.route('/empleado')
def empleado():
    return render_template("empleado.html")

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