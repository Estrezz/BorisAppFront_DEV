from flask import render_template, flash, redirect, url_for
from app import db
from app.models import Customer, Order, Producto, Company
from app.main.interface import buscar_pedido, buscar_alternativas, buscar_empresa, crea_envio, cotiza_envio, cargar_pedido, buscar_pedido_conNro, describir_variante, busca_tracking, validar_cobertura, crear_store, actualiza_json_categoria, actualiza_json, buscar_producto, agregar_nota, loguear_error, buscar_producto_nombre
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

    ########### Por si hace falta ver la Plataforma desde donde se llama ######################
    # plataforma = request.args.get('plataforma', 'Ninguna')
    empresa = request.args.get('store_id', 'Ninguna')

    if request.args.get('order_id') == None:
        return redirect(url_for('main.buscar', empresa = empresa))
    else: 
        unaEmpresa = buscar_empresa(empresa)
        ##### Empresa no existe ##################
        if unaEmpresa == "Failed":
            return render_template('no_encontrado.html')

        pedido = buscar_pedido_conNro(unaEmpresa, request.args.get('order_id'))
        cargar_pedido(unaEmpresa, pedido)
        return redirect(url_for('main.pedidos'))


############################## Search for company / order ################################
@bp.route('/buscar', methods=['GET', 'POST'])
def buscar():
    # Clean up old records
    for model in [Company, Order, Customer, Producto]:
        model.query.filter(model.timestamp <= datetime.utcnow() - timedelta(minutes=120)).delete()
    db.session.commit()

    # Clean up Session
    if 'uid' in session:
        Order.query.filter_by(order_uid=str(session['uid'])).delete()
        Customer.query.filter_by(customer_uid=str(session['uid'])).delete()
        Company.query.filter_by(company_uid=str(session['uid'])).delete()
        if 'orden' in session:
            Producto.query.filter_by(order_id=session['orden']).delete()
    db.session.commit()
    session.pop('orden', None)
    session.pop('cliente', None)
    session.pop('store', None)
    session.clear()

    # Get the value of 'empresa' from request arguments
    try:
        ID_empresa = request.args['empresa']
    except KeyError:
        return render_template('no_encontrado.html')

    # Look up the company in the database
    unaEmpresa = buscar_empresa(ID_empresa)
            
    # Handle POST requests to search for a specific order
    if request.method == "POST":
        ordernum = request.form.get("ordernum")
        ordermail = request.form.get('ordermail')

        if ordernum == '' or ordermail == '':
            flash('Por favor ingresá el Número de Orden y el Email')
            return render_template('buscar.html', title='Inicia tu gestión', empresa=unaEmpresa, textos=session.get('textos'))

        if not ordernum.isdigit():
            flash('Por favor ingresá el Número de Orden correctamente - Solo el número')
            return render_template('buscar.html', title='Inicia tu gestión', empresa=unaEmpresa, textos=session.get('textos'))

        pedido = buscar_pedido(unaEmpresa, ordernum, ordermail)
       
        if pedido == 'None' or pedido =='Reintentar':
            if pedido == 'None':
                flash('No se encontro un pedido para esa combinación Pedido-Email')
            if pedido == 'Reintentar':
                flash('No se pudo encontrar el pedido, por favor reintente en unso momentos')
            return render_template('buscar.html', title='Inicia tu gestión', empresa=unaEmpresa, textos=session.get('textos'))
        else:
            ##### Loguear error en pedido cuando aparece id = pedido['customer']['id'], TypeError: 'NoneType' object is not subscriptable
            if pedido is None:
                loguear_error("Buscar Pedido", "pedido es NoneType", ID_empresa, str(ordernum)+ordermail)
                flash('No se encontro un pedido para esa combinación Pedido-Email')
                return render_template('buscar.html', title='Inicia tu gestión', empresa=unaEmpresa, textos = session['textos'])
            cargar_pedido(unaEmpresa, pedido)
            return redirect(url_for('main.pedidos'))

    # Render the search page
    return render_template('buscar.html', title='Inicia tu Gestión', empresa=unaEmpresa, textos=session.get('textos'))



@bp.route('/pedidos', methods=['GET', 'POST'])
def pedidos():

    # Check if session has expired
    if 'cliente' not in session or not Customer.query.get(session['cliente']):
        return render_template('sesion_expirada.html')

    user = Customer.query.get(session['cliente'])
    company= user.pertenece
    order = Order.query.get(session['orden'])
    productos = Producto.query.filter_by(order_id=session['orden']).all()

    if request.method == "POST":
        form_item = request.form.get("form_item")
        prod_id = request.form.get("Prod_Id")
        item = Producto.query.get((session['orden'],prod_id))

        if form_item == "elegir_item" : 
            accion = request.form.get(str("accion"+request.form.get("Prod_Id")))
            accion_cantidad = request.form.get(str("accion_cantidad"+request.form.get("Prod_Id")))
            motivo = request.form.get(str("motivo"+request.form.get("Prod_Id")))

            item.accion = accion
            item.accion_reaccion = False 
            item.accion_cantidad = accion_cantidad
            item.motivo = motivo
            if request.form.get("observaciones"):
                item.observaciones = request.form.get("observaciones")

            db.session.commit()

            if accion == 'cambiar' and item.accion_reaccion == False:   
                alternativas = buscar_alternativas(company, session['store'], item.prod_id, item.variant)
                return render_template('devolucion.html', title='Cambio', empresa=company, NombreStore=company.company_name, user=user, order=order, item=item, alternativas=alternativas[0], atributos=alternativas[1], textos=session['textos'], lista_motivos=session['motivos'], cupon=session['cupon'], otracosa=session['otracosa'])

        elif form_item == "cambiar_item":
            opcion_cambio = request.form.get("opcion_cambio")
        
            ## Si se seleccionó cambio x VARIANTE
            if opcion_cambio == 'Variante':
                if request.form.get("variante"):
                    variante = ast.literal_eval(request.form.get("variante"))
                    item.accion_cambiar_por = variante['id']
                    item.accion_cambiar_por_prod_id = item.prod_id
                    ### Busca el nombre del producto  ###
                    producto_name = buscar_producto_nombre(company, session['store'], item.prod_id, item.variant)
                    item.accion_cambiar_por_desc = producto_name + " ("+ describir_variante(variante['values']) +")"

            ## Si se seleccionó cambio x CUPON
            elif opcion_cambio == 'Cupon':
                item.accion_cambiar_por = '1'
                item.accion_cambiar_por_prod_id = '1'
                item.accion_cambiar_por_desc = 'Cupón'
            ## Si se seleccionó el Boton de Otra Cosa

            elif opcion_cambio == 'otraCosa':  
                alternativa_select = request.form.get("alternativa_select")
            
                # Handle "No stock" case
                if alternativa_select == '0':
                    flash('No hay stock disponible para ese articulo')
                    item.accion = 'ninguna'
                    db.session.commit()
                    return render_template('pedido.html', title='Pedido', empresa=company,  NombreStore=company.company_name, user=user, order=order, productos=productos)

                # Handle if NONE is selected case
                elif alternativa_select is None:
                    flash('Debe seleccionar un producto' )
                    item.accion = 'ninguna'
                    db.session.commit() 
                    return render_template('pedido.html', title='Pedido', empresa=company,  NombreStore=company.company_name, user=user, order = order, productos = productos)

                ##### Si no se seleccionó ninguna variante
                elif alternativa_select == 'seleccionar':
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

            else:
                ## Si se seleccionó el Boton de VARIANTE pero no se seleccionó ningún articulo
                flash('Por favor, indica por que item queres realizar el cambio' )
                item.accion = 'ninguna'
                db.session.commit() 
                return render_template('pedido.html', title='Pedido', empresa=company, NombreStore=company.company_name, user=user, order = order, productos = productos)

        item.accion_reaccion = True
        db.session.commit() 
    
    return render_template('pedido.html', title='Pedido', empresa=company, NombreStore=company.company_name, user=user, order = order, productos = productos)


@bp.route('/pedidos_unitarios', methods=['GET', 'POST'])
def pedidos_unitarios():   
    ### prueba si la cookie expiro
    if not session.get('cliente'):
        return render_template('sesion_expirada.html')

    #company = Company.query.filter_by(store_id=session['store']).first()
    prod_id = request.form.get("Prod_Id")
    user = Customer.query.get(session['cliente'])
    company= user.pertenece
    order = Order.query.get(session['orden'])
    item = Producto.query.get((session['orden'], prod_id))
        
   
    return render_template('devolucion.html', title='Accion', empresa=company, NombreStore=company.company_name, user=user, order = order, item = item, textos=session['textos'],  lista_motivos=session['motivos'], cupon=session['cupon'])



@bp.route('/Confirmar',methods=['GET', 'POST'])
def confirma_cambios():
    ### prueba si la cookie expiro
    if not session.get('cliente'):
        return render_template('sesion_expirada.html')

    #company = Company.query.filter_by(store_id=session['store']).first()
    user = Customer.query.get(session['cliente'])
    #flash(user.email)

    ### prueba si la cookie expiro
    if not user:
        return render_template('sesion_expirada.html')

    company= user.pertenece
    order = Order.query.get(session['orden'])
    productos = db.session.query(Producto).filter((Producto.order_id==session['orden'])).filter((Producto.accion != 'ninguna'))
    ### Si no hay ninguna accion a realizar especificada
    if productos.count() == 0:
        flash('Por favor, especifica alguna acción a realizar')
        productos = Producto.query.filter_by(order_id=session['orden']).all()
        return render_template('pedido.html', title='Pedido', empresa=company, NombreStore=company.company_name, user=user, order = order, productos = productos)

    #############################################################################
    ### Si hay al menos un cambio de producto mara la orden entera como cambio
    #############################################################################
    salientes = 'No'
    for p in productos:
        if p.accion == 'cambiar' and  p.accion_cambiar_por_desc != 'Cupón' :
            salientes = 'Si'   
    order.salientes = salientes
    db.session.commit()
    

    ## ConCorreo - Appendear al diccionario precio_envio / area_valida
    for e in session['envio']:
        ##################################################################
        # valida si el código postal esta dentro del area aceptada 
        # La idea es que cada metodo de envio pueda tener un area valida
        ##################################################################

        if e['carrier'] != False:        
            precio_envio = cotiza_envio(company, user, order, productos, e)
            if precio_envio == 'Failed':
                precio_envio = 'A cotizar'
                area_valida = False
            else : 
                if e['costo_envio'] == "Merchant":
                    precio_envio = 'Sin Cargo'
                area_valida == True
        else:
            precio_envio = 0
            area_valida = True

        e['precio_envio'] = precio_envio
        e['area_valida'] = area_valida
        
    return render_template('pedido_confirmar.html', title='Confirmar', empresa=company, NombreStore=company.company_name, user=user, order = order, productos = productos, correo=company.correo_usado, area_valida=area_valida, textos=session['textos'], envio=session['envio'])



@bp.route('/direccion', methods=['GET', 'POST'])
def direccion():
    #company = Company.query.filter_by(store_id=session['store']).first()
     ### prueba si la cookie expiro
    if not session.get('cliente'):
        return render_template('sesion_expirada.html')

    user = Customer.query.get(session['cliente'])
    company= user.pertenece
       
    if request.method == "POST":
        user.name = request.form.get('user_name')
        user.email = request.form.get('user_mail')
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
        user = Customer.query.get(session['cliente'])

        return redirect(url_for('main.confirma_cambios'))
    return render_template('direccion.html',  empresa=company, user=user)



@bp.route('/confirma_solicitud', methods=['GET', 'POST'])
def confirma_solicitud():
    if not session.get('cliente'):
        return render_template('sesion_expirada.html')
    metodo_envio = request.args.get('metodo_envio')
    user = Customer.query.get(session['cliente'])
    company= user.pertenece
    order = Order.query.get(session['orden'])
    productos = db.session.query(Producto).filter((Producto.order_id == session['orden'])).filter((Producto.accion != 'ninguna'))

    # Selecciona de los metodos de envio disponibles para la tienda el que se seleccionó
    metodo = next(item for item in session['envio'] if item["metodo_envio_id"] == metodo_envio)
    
    if metodo['direccion_obligatoria'] == True and ((user.address == None or user.address == '') or (user.zipcode == None) ):        
        if request.args.get('area_valida') == 'True':
            area_valida = True
        else:
            area_valida = False
        flash("Por favor completa tus datos de contacto")
        return render_template('pedido_confirmar.html', title='Confirmar', empresa=company, NombreStore=company.company_name, user=user, order = order, productos = productos, correo=company.correo_usado, area_valida=area_valida, textos=session['textos'], envio=session['envio'])

    envio = crea_envio(company, user, order, productos, metodo)
    ##### Agrega nota en Orden Original
    agregar_nota(company, order)

    db.session.commit()

    return redirect(url_for('main.envio', envio=envio, metodo_envio=metodo_envio))


@bp.route('/envio(<envio>/<metodo_envio>',methods=['GET', 'POST'])
def envio( envio,metodo_envio ):
    ### prueba si la cookie expiro
    if not session.get('cliente'):
        return render_template('sesion_expirada.html')

    user = Customer.query.get(session['cliente'])
    ### prueba si la cookie expiro
    if not user:
        return render_template('sesion_expirada.html')

    company= user.pertenece
    order = Order.query.get(session['orden'])
    #### fin borrar session ? ####
    
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
    
    if not session.get('store'):
        return render_template('sesion_expirada.html')
    
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
    data = buscar_alternativas(company, company.store_id, prod_id, variant)

    #atributos_tmp = []
    #for i in data[1]:
    #    atributos_tmp.append(i)
    
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

    #atributos = json.dumps(atributos_tmp)
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