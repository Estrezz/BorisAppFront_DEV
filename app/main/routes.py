from flask import render_template, flash, redirect, url_for
from app import db
from app.models import Customer, Order, Producto, Company
from app.main.interface import buscar_pedido, buscar_alternativas, buscar_empresa, crea_envio, cotiza_envio, cargar_pedido, buscar_pedido_conNro, describir_variante, busca_tracking, validar_cobertura, crear_store, actualiza_json_categoria, actualiza_json, buscar_producto, agregar_nota
from app.main import bp
from flask import request, session
from datetime import datetime,timedelta
from os.path import exists
import os
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
        pedido = buscar_pedido_conNro(unaEmpresa, request.args.get('order_id'))
        cargar_pedido(unaEmpresa, pedido)
        return redirect(url_for('main.pedidos'))


@bp.route('/buscar', methods=['GET', 'POST'])
def buscar():

    ############## limpieza de Base #######################################
    #  Limpia todo lo que tiene mas de 120 minutos ########################
    # Ver que coincida con el tiempo de permanent session en config.py    #
    #######################################################################
    hoy = datetime.utcnow()
    old = hoy - timedelta(minutes=120)
    empresa_tmp = Company.query.filter(Company.timestamp <= old).all()
    orden_tmp = Order.query.filter(Order.timestamp <= old).all()
    cliente_tmp = Customer.query.filter(Customer.timestamp <= old).all()
    producto_tmp = Producto.query.filter(Producto.timestamp <= old).all()
   
    if(len(producto_tmp)) != 0:
        for p in producto_tmp:
            Producto.query.filter(Producto.timestamp <= old).delete()
            print('Se borarron productos',p)
    if(len(orden_tmp)) != 0:
        for o in orden_tmp:
            Order.query.filter(Order.timestamp <= old).delete()
            print('Se borarron ordenes',o)
    if(len(cliente_tmp)) != 0:
        for c in cliente_tmp:
            Customer.query.filter(Customer.timestamp <= old).delete()
            print('Se borarron clientes',c)
    if(len(empresa_tmp)) != 0:
        for e in empresa_tmp:
            Company.query.filter(Company.timestamp <= old).delete()
            print('Se borarron empresas',e)
    db.session.commit()
    ################################# fin limpieza ###########################

    if 'uid' in session:
        if 'orden' in session:
            Producto.query.filter_by(order_id=session['orden']).delete()
        Order.query.filter_by(order_uid=str(session['uid'])).delete()
        Customer.query.filter_by(customer_uid=str(session['uid'])).delete()
        Company.query.filter_by(company_uid=str(session['uid'])).delete()        
        db.session.commit()
        session.pop('orden', None)
        session.pop('cliente', None)
        session.pop('store', None)
        session.clear()

    ID_empresa = request.args['empresa']
    unaEmpresa = buscar_empresa(ID_empresa)

    if request.method == "POST":
        ordernum = request.form.get("ordernum")
        ordermail = request.form.get('ordermail')
        
        if ordernum == '' or ordermail == '':
            flash('Por favor ingresá el Número de Orden y el Email')
            return render_template('buscar.html', title='Inicia tu gestión', empresa=unaEmpresa, textos = session['textos'])
        
        if ordernum.isdigit():
            pedido = buscar_pedido(unaEmpresa, ordernum, ordermail)
        else:
            flash('Por favor ingresá el Número de Orden correctamente - Solo el número')
            return render_template('buscar.html', title='Inicia tu gestión', empresa=unaEmpresa, textos = session['textos'])

        #pedido = buscar_pedido(unaEmpresa, ordernum, ordermail)

        if pedido == 'None':
            flash('No se encontro un pedido para esa combinación Pedido-Email')
            return render_template('buscar.html', title='Inicia tu gestión', empresa=unaEmpresa, textos = session['textos'])
        else:
            cargar_pedido(unaEmpresa, pedido)
            return redirect(url_for('main.pedidos'))

    return render_template('buscar.html', title='Inicia tu Gestión', empresa=unaEmpresa, textos = session['textos'])



@bp.route('/pedidos', methods=['GET', 'POST'])
def pedidos():

    #company = Company.query.filter_by(store_id=session['store']).first()
    user = Customer.query.get(session['cliente'])
    company= user.pertenece
    order = Order.query.get(session['orden'])
    productos = Producto.query.filter_by(order_id=session['orden']).all()

    if request.method == "POST" and request.form.get("form_item") == "elegir_item" : 
        prod_id = request.form.get("Prod_Id")
        accion = request.form.get(str("accion"+request.form.get("Prod_Id")))
        accion_cantidad = request.form.get(str("accion_cantidad"+request.form.get("Prod_Id")))
        motivo = request.form.get(str("motivo"+request.form.get("Prod_Id")))
        item = Producto.query.get((session['orden'],prod_id))
        item.accion = accion
        item.accion_reaccion = False 
        item.accion_cantidad = accion_cantidad
        item.motivo = motivo
        db.session.commit()

        if accion == 'cambiar' and item.accion_reaccion == False:   
            user = Customer.query.get(session['cliente'])
            order = Order.query.get(session['orden'])
            item = Producto.query.get((session['orden'],prod_id))
            alternativas = buscar_alternativas(company, session['store'], item.prod_id, item.variant, 'variantes')
            return render_template('devolucion.html', title='Cambio', empresa=company, NombreStore=company.company_name, user=user, order=order, item=item, alternativas=alternativas[0], atributos=alternativas[1], textos=session['textos'], lista_motivos=session['motivos'], cupon=session['cupon'], otracosa=session['otracosa'])

    if request.method == "POST" and request.form.get("form_item") == "cambiar_item" :
        prod_id = request.form.get("Prod_Id")
        opcion_cambio = request.form.get("opcion_cambio")
        item = Producto.query.get((session['orden'],prod_id))
        ## Si se seleccionó el Boton de VARIANTE
        if opcion_cambio == 'Variante':
            if request.form.get("variante"):
                variante = ast.literal_eval(request.form.get("variante"))
                item.accion_cambiar_por = variante['id']
                item.accion_cambiar_por_prod_id = item.prod_id
                ### Busca el nombre del producto  ###
                producto_name = buscar_alternativas(company, session['store'], item.prod_id, item.variant,'nombre')
                item.accion_cambiar_por_desc = producto_name + " ("+ describir_variante(variante['values']) +")"
            else:
                ## Si se seleccionó el Boton de VARIANTE pero no se seleccionó ningún articulo
                flash('Por favor, indica por que item queres realizar el cambio' )
                item.accion = 'ninguna'
                db.session.commit() 
                return render_template('pedido.html', title='Pedido', empresa=company, NombreStore=company.company_name, user=user, order = order, productos = productos)

        ## Si se seleccionó el Boton de CUPON
        if opcion_cambio == 'Cupon':
            item.accion_cambiar_por = '1'
            item.accion_cambiar_por_prod_id = '1'
            item.accion_cambiar_por_desc = 'Cupón'

        ## Si se seleccionó el Boton de Otra Cosa
        if opcion_cambio == 'otraCosa':
            ##### Si no hay stock del articulo seleccionado"
            if request.form.get("alternativa_select") == '0':
                flash('No hay stock disponible para ese articulo' )
                item.accion = 'ninguna'
                db.session.commit() 
                return render_template('pedido.html', title='Pedido', empresa=company,  NombreStore=company.company_name, user=user, order = order, productos = productos)

            ##### Si no se seleccionó ninguna producto
            if request.form.get("alternativa_select") == None:
                flash('Debe seleccionar un producto' )
                item.accion = 'ninguna'
                db.session.commit() 
                return render_template('pedido.html', title='Pedido', empresa=company,  NombreStore=company.company_name, user=user, order = order, productos = productos)

            ##### Si no se seleccionó ninguna variante
            if request.form.get("alternativa_select") == 'seleccionar':
                flash('Debe seleccionar alguna variante ' )
                item.accion = 'ninguna'
                db.session.commit() 
                return render_template('pedido.html', title='Pedido', empresa=company, NombreStore=company.company_name, user=user, order = order, productos = productos)

            variante_id = request.form.get("alternativa_select")
            producto = request.form.get("producto_nombre")
            variante = request.form.get("variante_nombre")
            producto_id = request.form.get("producto_id")
            
            item.accion_cambiar_por = variante_id
            item.accion_cambiar_por_prod_id = producto_id
            item.accion_cambiar_por_desc = producto+"("+variante+")"

        item.accion_reaccion = True
        db.session.commit() 
    
    return render_template('pedido.html', title='Pedido', empresa=company, NombreStore=company.company_name, user=user, order = order, productos = productos)


@bp.route('/pedidos_unitarios', methods=['GET', 'POST'])
def pedidos_unitarios():   

    #company = Company.query.filter_by(store_id=session['store']).first()
    prod_id = request.form.get("Prod_Id")
    user = Customer.query.get(session['cliente'])
    company= user.pertenece
    order = Order.query.get(session['orden'])
    item = Producto.query.get((session['orden'], prod_id))
    
    #if request.method == "POST": 
    #    company = Company.query.filter_by(store_id=session['store']).first()
    #    prod_id = request.form.get("Prod_Id")
    #    user = Customer.query.get(session['cliente'])
    #    order = Order.query.get(session['orden'])
    #    item = Producto.query.get((session['orden'], prod_id))
    return render_template('devolucion.html', title='Accion', empresa=company, NombreStore=company.company_name, user=user, order = order, item = item, textos=session['textos'],  lista_motivos=session['motivos'], cupon=session['cupon'])



@bp.route('/Confirmar',methods=['GET', 'POST'])
def confirma_cambios():
    ### prueba si la cookie expiro
    if not session.get('cliente'):
        flash('La sesion expiro, por favor entre al portal nuevamente')
        return render_template('sesion_expirada.html')
    #company = Company.query.filter_by(store_id=session['store']).first()
    user = Customer.query.get(session['cliente'])
    company= user.pertenece
    order = Order.query.get(session['orden'])
    productos = db.session.query(Producto).filter((Producto.order_id==session['orden'])).filter((Producto.accion != 'ninguna'))
    ### Si no hay ninguna accion a realizar especificada
    if productos.count() == 0:
        flash('Por favor, especifica alguna acción a realizar')
        productos = Producto.query.filter_by(order_id=session['orden']).all()
        return render_template('pedido.html', title='Pedido', empresa=company, NombreStore=company.company_name, user=user, order = order, productos = productos)

    
    ## ConCorreo - Appendear al diccionario precio_envio / area_valida
    for e in session['envio']:
        ##############################################################
        # valida si el código postal esta dentro del area aceptada 
        # La idea es que cada metodo de envio pueda tener un area valida
        #############################################################
        

        if e['carrier'] != False:           
            area_valida = validar_cobertura(user.province, user.zipcode)
            if e['costo_envio'] == "Merchant":
                precio_envio = 'Sin Cargo'
            else: 
                precio_envio = cotiza_envio(company, user, order, productos, e)
                if precio_envio == 'Failed':
                    precio_envio = 'A cotizar'
        else:
            precio_envio = 0
            area_valida = True

        e['precio_envio'] = precio_envio
        e['area_valida'] = area_valida
        
    #precio_envio = cotiza_envio(company, user, order, productos, company.correo_usado)
    

    #############################################################################
    ### Si hay al menos un cambio de producto mara la orden entera como cambio
    #############################################################################
    salientes = 'No'
    for p in productos:
        if p.accion == 'cambiar' and  p.accion_cambiar_por_desc != 'Cupón' :
            salientes = 'Si'   
    order.salientes = salientes
    db.session.commit()
    return render_template('pedido_confirmar.html', title='Confirmar', empresa=company, NombreStore=company.company_name, user=user, order = order, productos = productos, correo=company.correo_usado, area_valida=area_valida, textos=session['textos'], envio=session['envio'])



@bp.route('/direccion', methods=['GET', 'POST'])
def direccion():
    #company = Company.query.filter_by(store_id=session['store']).first()
    user = Customer.query.get(session['cliente'])
    company= user.pertenece
       
    if request.method == "POST":
        user.name = request.form.get('user_name')
        user.mail = request.form.get('user_mail')
        user.phone = request.form.get('user_phone')
        user.address = request.form.get('user_address')
        user.number = request.form.get('user_number')
        user.floor = request.form.get('user_floor')
        user.locality = request.form.get('user_locality')
        user.zipcode = request.form.get('user_zipcode')
        user.city = request.form.get('user_city')
        user.province = request.form.get('user_province')
        user.country = request.form.get('user_country')
        user.instructions = request.form.get('user_instructions')
        
        db.session.commit() 
        return redirect(url_for('main.confirma_cambios'))
    return render_template('direccion.html',  empresa=company, user=user)



@bp.route('/confirma_solicitud', methods=['GET', 'POST'])
def confirma_solicitud():
    metodo_envio = request.args.get('metodo_envio')
    #company = Company.query.filter_by(store_id=session['store']).first()
    user = Customer.query.get(session['cliente'])
    company= user.pertenece
    order = Order.query.get(session['orden'])
    productos = db.session.query(Producto).filter((Producto.order_id == session['orden'])).filter((Producto.accion != 'ninguna'))
    
    #### valida que la dirección esta cargada si el método elegido es A Coordinar o Moova ################
    

    # Selecciona de los metodos de envio disponibles para la tienda el que se seleccionó
    metodo = next(item for item in session['envio'] if item["metodo_envio_id"] == metodo_envio)
    

    if metodo['direccion_obligatoria'] == 'Si' and ((user.address == None or user.address == '') or (user.zipcode == None) ):        
        if request.args.get('area_valida') == 'True':
            area_valida = True
        else:
            area_valida = False
        flash("Por favor completa tus datos de contacto")
        return render_template('pedido_confirmar.html', title='Confirmar', empresa=company, NombreStore=company.company_name, user=user, order = order, productos = productos, correo=company.correo_usado, area_valida=area_valida, textos=session['textos'], envio=session['envio'])

    envio = crea_envio(company, user, order, productos, metodo)
    ##### Agrega nota en Orden Original
    agregar_nota(company, order)

    #### borra el pedido de la base
    #Producto.query.filter_by(order_id=session['orden']).delete()
    #Order.query.filter_by(order_uid=str(session['uid'])).delete()
    #Customer.query.filter_by(customer_uid=str(session['uid'])).delete()

    db.session.commit()
    
    #return render_template('envio.html', empresa=company, NombreStore=company.company_name, company=company, user=user, order=order, envio=envio, metodo_envio=metodo_envio, textos=session['textos'])
    return redirect(url_for('main.envio', envio=envio, metodo_envio=metodo_envio))


@bp.route('/envio(<envio>/<metodo_envio>',methods=['GET', 'POST'])
def envio( envio,metodo_envio ):
    ### prueba si la cookie expiro
    if not session.get('cliente'):
        flash('La sesion expiro, por favor entre al portal nuevamente')
        return render_template('sesion_expirada.html')
    user = Customer.query.get(session['cliente'])
    company= user.pertenece
    order = Order.query.get(session['orden'])
    return render_template('envio.html', empresa=company, user=user, order=order, envio=envio, metodo_envio=metodo_envio, textos=session['textos'])


@bp.route('/tracking/<order>',methods=['GET', 'POST'])
def tracking(order):
    historia = busca_tracking(order)
    empresa = {}
    return render_template('tracking.html', empresa=empresa,  title='Tracking', historia=historia)



@bp.route('/empresa/crear', methods=['POST'])
def crear_empresa():
    if request.method == 'POST':
        store = request.json
        
        actualiza = crear_store(store)

        if actualiza == 'Success':
            return '', 200
        else:
            return 'Error - Ya existe el JSON',400


@bp.route('/empresa_categorias', methods=['POST'])
def actualizar_empresa_categorias():
    if request.method == 'POST':
        data = request.json
        #empresa = Company.query.filter_by(store_id=data['store_id']).first()
        param_config = 'app/static/conf/'+data['store_id']+'.json'

        status = actualiza_json_categoria(param_config, data)
        if status == 'Success':
            return '', 200
        else:
            return 'Error',400


@bp.route('/empresa_json', methods=['POST'])
def actualizar_empresa_json():
    if request.method == 'POST':
        data = request.json
        clave = request.args.get('clave')
        
        if request.args.get('key'):
            key = request.args.get('key')
        else:
            key='textos'

        #empresa = Company.query.filter_by(store_id=data['store_id']).first()
        param_config = 'app/static/conf/'+data['store_id']+'.json'

        status = actualiza_json(param_config, clave, data, key)
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


    
@bp.route('/recibir_imagen', methods=['POST'])
def recibir_imagen():
    if request.method == 'POST':
        file = request.files['image']
        filename =  file.filename
        if exists('app/static/images/background/'+filename):
            os.remove('app/static/images/background/'+filename)
            file.save('app/static/images/background/'+filename)
        else:
            file.save('app/static/images/background/'+filename)
        return 'Success'