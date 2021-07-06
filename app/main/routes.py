from flask import render_template, flash, redirect, url_for, jsonify
from app import db
from app.main.forms import LoginForm, DireccionForm
from app.email import send_email
from app.models import Store, Customer, Order, Producto, Company
from app.main.interface import buscar_pedido, buscar_promo, buscar_alternativas, buscar_empresa, crea_envio, cotiza_envio, cargar_pedido, buscar_pedido_conNro, describir_variante, busca_tracking, validar_cobertura, actualizar_store, crear_store, actualiza_json_categoria, actualiza_json, buscar_producto, agregar_nota
from app.main import bp
from flask import request, session
import requests
import json
import ast


@bp.route('/', methods=['GET', 'POST'])

@bp.route('/home', methods=['GET', 'POST'])
def home():

    if request.args.get('store_id') == None:
        empresa ='Ninguna'
    else: 
        empresa = request.args.get('store_id')

    if request.args.get('order_id') == None:
        return redirect(url_for('main.buscar', empresa = empresa))
    else: 
        unaEmpresa = buscar_empresa(empresa)
        ## cambios
        pedido = buscar_pedido_conNro(unaEmpresa, request.args.get('order_id'))
        cargar_pedido(unaEmpresa, pedido)
        return redirect(url_for('main.pedidos'))


@bp.route('/buscar', methods=['GET', 'POST'])
def buscar():
    ## Borrar todos los datos de la base de datos ##
    if 'orden' in session:
        Producto.query.filter_by(order_id=session['orden']).delete()
        Order.query.filter_by(id=session['orden']).delete()
        Customer.query.filter_by(id=session['cliente']).delete()
        #cust_tmp = Customer.query.filter_by(id=session['cliente']).delete()
        #db.session.delete(cust_tmp)
        Company.query.filter_by(store_id=session['store']).delete()
        db.session.commit()
        session.pop('orden', None)
        session.pop('cliente', None)
        session.pop('store', None)
        session.clear()


    # Company.query.delete()
    # Customer.query.delete()
    # Order.query.delete()
    # Producto.query.delete()
    # db.session.commit()
    #### fin borrado #################################

    unaEmpresa = buscar_empresa(request.args['empresa'])

    form = LoginForm()
    if form.validate_on_submit():
        ## cambios
        pedido = buscar_pedido(unaEmpresa, form)

        if pedido == 'None':
            flash('No se encontro un pedido para esa combinación Pedido-Email')
            return render_template('buscar.html', title='Inicia tu gestión', NombreStore=unaEmpresa.company_name, form=form, store=unaEmpresa.company_name, logo=unaEmpresa.logo)
        else:
            cargar_pedido(unaEmpresa, pedido)
            return redirect(url_for('main.pedidos'))

    return render_template('buscar.html', title='Inicia tu Gestión', NombreStore=unaEmpresa.company_name, form=form, store=unaEmpresa.company_name, logo=unaEmpresa.logo)



@bp.route('/pedidos', methods=['GET', 'POST'])
def pedidos():

    company = Company.query.filter_by(store_id=session['store']).first()
    user = Customer.query.get(session['cliente'])
    order = Order.query.get(session['orden'])
    productos = Producto.query.filter_by(order_id=session['orden']).all()

    if request.method == "POST" and request.form.get("form_item") == "elegir_item" : 
        prod_id = request.form.get("Prod_Id")
        accion = request.form.get(str("accion"+request.form.get("Prod_Id")))
        accion_cantidad = request.form.get(str("accion_cantidad"+request.form.get("Prod_Id")))
        motivo = request.form.get(str("motivo"+request.form.get("Prod_Id")))
        item = Producto.query.get(prod_id)
        item.accion = accion
        item.accion_reaccion = False 
        item.accion_cantidad = accion_cantidad
        item.motivo = motivo
        db.session.commit()

        if accion == 'cambiar' and item.accion_reaccion == False:   
            user = Customer.query.get(session['cliente'])
            order = Order.query.get(session['orden'])
            item = Producto.query.get(prod_id)
            alternativas = buscar_alternativas(company, session['store'], item.prod_id, item.variant, 'variantes')
            return render_template('devolucion.html', title='Cambio', NombreStore=company.company_name, user=user, order=order, item=item, alternativas=alternativas[0], atributos=alternativas[1], textos=session['textos'], lista_motivos=session['motivos'], cupon=session['cupon'], otracosa=session['otracosa'])

    if request.method == "POST" and request.form.get("form_item") == "cambiar_item" :
        prod_id = request.form.get("Prod_Id")
        opcion_cambio = request.form.get("opcion_cambio")
        item = Producto.query.get(prod_id)
        ## Si se seleccionó el Boton de VARIANTE
        if opcion_cambio == 'Variante':
            if request.form.get("variante"):
                variante = ast.literal_eval(request.form.get("variante"))
                item.accion_cambiar_por = variante['id']
                ### Busca el nombre del producto  ###
                producto_name = buscar_alternativas(company, session['store'], item.prod_id, item.variant,'nombre')
                item.accion_cambiar_por_desc = producto_name + " ("+ describir_variante(variante['values']) +")"
            else:
                ## Si se seleccionó el Boton de VARIANTE pero no se seleccionó ningún articulo
                flash('Por favor, indica por que item queres realizar el cambio' )
                item.accion = 'ninguna'
                db.session.commit() 
                return render_template('pedido.html', title='Pedido', NombreStore=company.company_name, user=user, order = order, productos = productos)

        ## Si se seleccionó el Boton de CUPON
        if opcion_cambio == 'Cupon':
            item.accion_cambiar_por = '1'
            item.accion_cambiar_por_desc = 'Cupón'

        ## Si se seleccionó el Boton de Otra Cosa
        if opcion_cambio == 'otraCosa':
            variante_id = request.form.get("alternativa_select")
            producto = request.form.get("producto_nombre")
            variante = request.form.get("variante_nombre")
            item.accion_cambiar_por = variante_id
            item.accion_cambiar_por_desc = producto+"("+variante+")"

        item.accion_reaccion = True
        db.session.commit() 

    return render_template('pedido.html', title='Pedido', NombreStore=company.company_name, user=user, order = order, productos = productos)


@bp.route('/pedidos_unitarios', methods=['GET', 'POST'])
def pedidos_unitarios():   
    if request.method == "POST": 
        company = Company.query.filter_by(store_id=session['store']).first()
        prod_id = request.form.get("Prod_Id")
        user = Customer.query.get(session['cliente'])
        order = Order.query.get(session['orden'])
        item = Producto.query.get(prod_id)
    return render_template('devolucion.html', title='Accion', NombreStore=company.company_name, user=user, order = order, item = item, textos=session['textos'],  lista_motivos=session['motivos'], cupon=session['cupon'])



@bp.route('/Confirmar',methods=['GET', 'POST'])
def confirma_cambios():
    company = Company.query.filter_by(store_id=session['store']).first()
    user = Customer.query.get(session['cliente'])
    order = Order.query.get(session['orden'])
    productos = db.session.query(Producto).filter((Producto.order_id==session['orden'])).filter((Producto.accion != 'ninguna'))
    ### Si no hay ninguna accion a realizar especificada
    if productos.count() == 0:
        flash('Por favor, especifica alguna acción a realizar')
        productos = Producto.query.filter_by(order_id=session['orden']).all()
        return render_template('pedido.html', title='Pedido', NombreStore=company.company_name, user=user, order = order, productos = productos)

    precio_envio = cotiza_envio(company, user, order, productos, company.correo_usado)
    area_valida = validar_cobertura(user.province, user.zipcode)

    return render_template('pedido_confirmar.html', title='Confirmar', NombreStore=company.company_name, user=user, order = order, productos = productos, precio_envio=precio_envio, correo=company.correo_usado, area_valida=area_valida, textos=session['textos'], envio=session['envio'])



@bp.route('/direccion', methods=['GET', 'POST'])
def direccion():
    user = Customer.query.get(session['cliente'])
    form = DireccionForm()
    if request.method == 'GET':
        form.name.data = user.name
        form.email.data = user.email
        form.phone.data = user.phone
        form.address.data = user.address
        form.number.data = user.number
        form.floor.data = user.floor
        form.zipcode.data = user.zipcode
        form.locality.data = user.locality
        form.city.data = user.city
        form.province.data = user.province
        form.country.data = user.country
    if form.validate_on_submit():
        form.populate_obj(obj=user)
        db.session.commit() 
        return redirect(url_for('main.confirma_cambios'))
    return render_template('direccion.html', form=form, user=user)



@bp.route('/confirma_solicitud', methods=['GET', 'POST'])
def confirma_solicitud():
    metodo_envio = request.args.get('metodo_envio')
    company = Company.query.filter_by(store_id=session['store']).first()
    user = Customer.query.get(session['cliente'])
    order = Order.query.get(session['orden'])
    productos = db.session.query(Producto).filter((Producto.order_id == session['orden'])).filter((Producto.accion != 'ninguna'))
    
    envio = crea_envio(company, user, order, productos, metodo_envio)
    ##### Agrega nota en Orden Original
    agregar_nota(company, order)
    #### borra el pedido de la base
    Producto.query.filter_by(order_id=session['orden']).delete()
    Order.query.filter_by(id=session['orden']).delete()
    Customer.query.filter_by(id=session['cliente']).delete()
    db.session.commit()
    
    return render_template('envio.html', NombreStore=company.company_name, company=company, user=user, order=order, envio=envio, metodo_envio=metodo_envio, textos=session['textos'])


@bp.route('/tracking/<order>',methods=['GET', 'POST'])
def tracking(order):
    historia = busca_tracking(order)
    return render_template('tracking.html', title='Tracking', historia=historia)



@bp.route('/empresa/chequear', methods=['POST'])
def chequear_empresa():
    if request.method == 'POST':
        store = request.json
        
        actualiza = 'Failed'
        if Store.query.filter_by(store_id=store['store_id']).first():
            actualiza = actualizar_store(store)
        else:
           actualiza = crear_store(store)

        if actualiza == 'Success':
            return '', 200
        else:
            return 'Error',400


@bp.route('/empresa_categorias', methods=['POST'])
def actualizar_empresa_categorias():
    if request.method == 'POST':
        data = request.json
        store = Store.query.filter_by(store_id=data['store_id']).first()

        status = actualiza_json_categoria(store.param_config, data)
        if status == 'Success':
            return '', 200
        else:
            return 'Error',400


@bp.route('/empresa_json', methods=['POST'])
def actualizar_empresa_json():
    if request.method == 'POST':
        data = request.json
        clave = request.args.get('clave')
        store = Store.query.filter_by(store_id=data['store_id']).first()

        status = actualiza_json(store.param_config, clave, data)
        if status == 'Success':
            return '', 200
        else:
            return 'Error',400
        

@bp.route('/elegir_producto', methods=['POST'])
def elegir_producto():
    desc_prod = request.form.get('prod')
    company = Company.query.filter_by(store_id=session['store']).first()
    producto = buscar_producto(company, desc_prod)
    if type(producto) == dict:
        return json.dumps({'success':False}), 400, {'ContentType':'application/json'} 
    return json.dumps(producto)



@bp.route('/elegir_alternativa', methods=['POST'])
def elegir_alternativa():
    prod_id = request.form.get('prod_id')
    variant = 0
    company = Company.query.filter_by(store_id=session['store']).first()
    data = buscar_alternativas(company, company.store_id, prod_id, variant, 'variantes')

    atributos_tmp = []
    for i in data[1]:
        atributos_tmp.append(i['es'])
    
    alternativas_tmp = []
   
    for i in data[0]:
        alternativa_id = i['id']
        alternativa_desc = ""
        for x in i['values']:
            if alternativa_desc == "":
                alternativa_desc = str(x['es'])
            else:
                alternativa_desc = alternativa_desc +','+ str(x['es'])
        alternativas_tmp.append({'id': alternativa_id,'desc': alternativa_desc})

    atributos = json.dumps(atributos_tmp)
    alternativas = json.dumps(alternativas_tmp)

    return alternativas
