
import re
import traceback
import datetime
# from flask_bootstrap import Bootstrap
from flask import (Flask, flash, g, make_response, redirect, render_template,
                   request, url_for)
#from Forms import ClienteForm
#from Forms import ClienteForm
from flask_wtf import CsrfProtect
from flask_wtf.csrf import CSRFProtect

import Forms
from config import DevelopmentConfig
# from Forms import ProveedorForm
from models import (db, empleado, pago, pedido, producto, productoTerminado,
                    proveedor, rol, usuario, venta, producto_T)

csrf = CSRFProtect()

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
# bootstrap=Bootstrap(app)

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
    return render_template("proveedoresIna.html", proveedores=getAllProIna,)


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
    
    return render_template("inventarioMaterial.html", materiales=materiales, idMaterial=idMaterial)


@app.route('/productos')
def productos():
    productos = productoTerminado.query.filter(productoTerminado.fecha_registro==datetime.date.today(), productoTerminado.estatus==1).all()
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
