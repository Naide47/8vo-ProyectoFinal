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

"""@app.route('/pedidos/agregar', methods=["POST","GET"])
def pedidosAgregar():
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
    
    return render_template("pedidos.html")"""

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