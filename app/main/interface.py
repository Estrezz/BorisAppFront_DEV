import requests
import json
import datetime
import smtplib
from datetime import datetime
from app import db
from app.models import Customer, Order, Producto, Company, Store
from flask import session, flash, current_app, render_template
from app.main.moova import crea_envio_moova, cotiza_envio_moova
from app.main.tiendanube import buscar_pedido_tiendanube, buscar_pedido_conNro_tiendanube, buscar_alternativas_tiendanube
from app.email import send_email


def buscar_nro_pedido(lista, valor):
    for x in lista:
     if x['number'] == valor:
          return x
    else:
     return 'None'


def buscar_pedido(empresa, form):
  if empresa.platform == 'tiendanube':
    order_tmp = buscar_pedido_tiendanube(empresa, form)
    

  if type(order_tmp) == dict:
    return 'None'
  else:
    order = buscar_nro_pedido(order_tmp, form.ordernum.data)
    return order


def buscar_pedido_conNro(empresa, orderid):
  if empresa.platform == 'tiendanube':
    order = buscar_pedido_conNro_tiendanube(empresa, orderid)
  
  
  return order


#############################################################################
# Busca la promo con la que se vendió un articulo 
# devuelve [nombre promo. precio promocional]
#############################################################################
def buscar_promo(promociones, Id_Producto ):
  promo = ("",0,0)
  for x in promociones: 
    if x['id'] == Id_Producto:
      promo = (x['discount_script_type'], x['discount_amount'], x['final_price'])
      return promo
  return promo
  

#####################################################################################################
# Busca alternativas para cambiar un articulo según el motivo de cambio
# devuelve lista con productos alternativos y le oden de los atributos (para tener como encabezados)
#####################################################################################################
def buscar_alternativas(company, storeid, prod_id, item_variant, param):
  if company.platform == 'tiendanube':
    product = buscar_alternativas_tiendanube(company, storeid, prod_id)
  
  variantes = []

  if param == "nombre":
    return product['name']['es']
  
  for x in product['variants']:
    # validar stock infinito (NoneType) y permitir cambiar por lo mismo
    # if x['stock'] > 1 and x['id'] != item_variant :
    if isinstance(x['stock'], type(None)) == True:
      if x['id'] == item_variant:
        x['values']= [{"es": "Mismo Articulo"}]
      variantes.append(x)
    else: 
      if x['stock'] > 1 :
        if x['id'] == item_variant:
          x['values']= [{"es": "Mismo Articulo"}]
        variantes.append(x)
  
  ## cambio para ver si no existen variantes del producto

  devolver = [variantes, product['attributes']]
  return devolver

############################## describir_variante ##################################################
## Arma string con las descripcion de las variantes
def describir_variante(values):
  desc = ''
  for i in values:
    if desc != '':
      desc = desc + ' - '
    desc = desc + i['es'] 
  return desc

############################## buscar_empresa ##################################################
def buscar_empresa(empresa):
  if empresa != 'Ninguna':
    empresa_tmp = Store.query.filter(Store.store_id == empresa).first()
    #### guarda settings de la empresa
    settings = guardar_settings(empresa_tmp.param_config)
    session['shipping'] = settings['shipping']
    session['test'] = settings['test']
    session['correo_test'] = settings['correo_test']
    session['provincia_codigos_postales'] = settings['provincia_codigos_postales']
    session['ventana_cambio'] = settings['politica']['ventana_cambio']
    session['ventana_devolucion'] = settings['politica']['ventana_devolucion']
    session['textos'] = settings['textos']
    session['envio'] = settings['envio']
    session['motivos'] = settings['motivos']

    unaEmpresa = Company(
      platform = empresa_tmp.platform,
      store_id = empresa_tmp.store_id,
      platform_token_type = empresa_tmp.platform_token_type,
      platform_access_token = empresa_tmp.platform_access_token,
      company_name = empresa_tmp.store_name,
      company_url = empresa_tmp.store_url,
      company_country = empresa_tmp.store_country,
      company_main_language = empresa_tmp.store_main_language,
      company_main_currency = empresa_tmp.store_main_currency,
      admin_email = empresa_tmp.admin_email,
      communication_email = empresa_tmp.communication_email,
      logo = empresa_tmp.param_logo,
      correo_usado = empresa_tmp.correo_usado,
      correo_apikey = empresa_tmp.correo_apikey,
      correo_id = empresa_tmp.correo_id,
      correo_test = empresa_tmp.correo_test,
      correo_apikey_test = empresa_tmp.correo_apikey_test,
      correo_id_test = empresa_tmp.correo_id_test,
      contact_name = empresa_tmp.contact_name,
      contact_email = empresa_tmp.contact_email,
      contact_phone = empresa_tmp.contact_phone,
      shipping_address = empresa_tmp.shipping_address,
      shipping_number = empresa_tmp.shipping_number,
      shipping_floor = empresa_tmp.shipping_floor,
      shipping_zipcode = empresa_tmp.shipping_zipcode,
      shipping_city = empresa_tmp.shipping_city,
      shipping_province = empresa_tmp.shipping_province,
      shipping_country = empresa_tmp.shipping_country,
      shipping_info = empresa_tmp.shipping_info
    )
  else: 
    settings = guardar_settings('app/static/conf/boris.json')
    session['shipping'] = settings['shipping']
    session['test'] = settings['test']
    session['correo_test'] = settings['correo_test']
    session['provincia_codigos_postales'] = settings['provincia_codigos_postales']
    session['ventana_cambio'] = settings['politica']['ventana_cambio']
    session['ventana_devolucion'] = settings['politica']['ventana_devolucion']
    session['textos'] = settings['textos']
    session['envio'] = settings['envio']
    session['motivos'] = settings['motivos']

    unaEmpresa = Company(
      platform = 'tiendanube',
      platform_access_token = 'cb9d4e17f8f0c7d3c0b0df4e30bcb2b036399e16',
      platform_token_type = 'bearer',
      store_id = '1447373',
      company_country = 'AR',
      company_main_language = 'es',
      company_main_currency = 'ARS',
      communication_email = 'info@borisreturns.com',
      company_name = 'Tu Tienda',
      company_url= 'https://demoboris.mitiendanube.com',
      admin_email = 'info@borisreturns.com',
      logo = 'https://frontprod.borisreturns.com/static/images/Boris_Naranja.png',
      correo_usado = 'Moova',
      correo_apikey = 'b23920003684e781d87e7e5b615335ad254bdebc',
      correo_id = 'b22bc380-439f-11eb-8002-a5572ae156e7',
      correo_test = True,
      correo_apikey_test = 'b23920003684e781d87e7e5b615335ad254bdebc',
      correo_id_test = 'b22bc380-439f-11eb-8002-a5572ae156e7',
      contact_name = 'Almacen Tienda',
      contact_email = 'info@borisreturns.com',
      contact_phone = '+5491151064817',
      shipping_address = 'Virrey Loreto',
      shipping_number = '2259',
      shipping_floor = '',
      shipping_zipcode = '1426',
      shipping_city = 'CABA',
      shipping_province = 'CABA',
      shipping_country = 'AR',
      shipping_info = 'Entregar en recepción'
    )
  return unaEmpresa


################################# guardar_settings ##########################################
##################### Carga el archivo de settings desde el campo param_config ##############
############################## de la base de empresas #######################################
def guardar_settings(url):
  with open(url, encoding='utf-8') as json_file:
    data = json.load(json_file)
    return data


############################## crea_envio ##################################################
def crea_envio(company, user, order, productos, metodo_envio): 
  if metodo_envio == 'Moova':
    solicitud_envio = crea_envio_moova(company, user, order, productos)
    if solicitud_envio == 'Failed':
      return 'Failed'
  else:
    solicitud_envio = {
      "id":'Manual',
      "status":'DRAFT',
      "price":'0.0',
      "priceFormatted":'0.0',
      "currency":'ARS'
    }

  mandaBoris = almacena_envio(company, user, order, productos, solicitud_envio, metodo_envio)
  if mandaBoris == 'Error':
    flash('ya existe un cambio para esa orden')
  else: 
    ## agregado try / except
    try:
      send_email('Tu orden ha sido iniciada', 
                #sender=current_app.config['ADMINS'][0], 
                sender=company.communication_email,
                recipients=[user.email], 
                text_body=render_template('email/pedido_listo.txt',
                                         user=user, company=company, productos=productos, envio=solicitud_envio, order=order, shipping=session['shipping'], metodo_envio=metodo_envio),
                html_body=render_template('email/pedido_listo.html',
                                         user=user, company=company, productos=productos, envio=solicitud_envio, order=order, shipping=session['shipping'], metodo_envio=metodo_envio), 
                attachments=None, 
                sync=False,
                bcc=[current_app.config['ADMINS'][0]])
    except smtplib.SMTPException as e:
      error_mail = e
      flash('Mensaje {}'.format('a.error_mail'))

    send_email('Se ha generado una orden en Boris', 
                sender=company.communication_email,
                #sender=current_app.config['ADMINS'][0], 
                recipients=[company.communication_email], 
                text_body=render_template('email/nuevo_pedido.txt',
                                         user=user, envio=solicitud_envio, order=order, shipping=session['shipping']),
                html_body=render_template('email/nuevo_pedido.html',
                                         user=user, envio=solicitud_envio, order=order, shipping=session['shipping']), 
                attachments=None, 
                sync=False,
                bcc=[current_app.config['ADMINS'][0]])
  return solicitud_envio


############################## cotiza_envio ##################################################
#### Cotizar el precio del envío
def cotiza_envio(company, user, order, productos, correo):
  if 'shipping' in session:  
    if session['shipping'] == 'company':
      return 'Retiro Gratuito'

  if correo == 'Moova':
    precio = cotiza_envio_moova (company, user, order, productos)
    return precio

  return 'Failed'



############################## almacena_envio ##################################################
def almacena_envio(company, user, order, productos, solicitud, metodo_envio):
  if 'test' in session:  
    if session['test'] == 'True':
      url='../Boris_common/logs/pedido'+str(order.id)+'.json'
    else: 
      if current_app.config['SERVER_ROLE'] == 'DEV':
        url="http://back.borisreturns.com/pedidos"
      if current_app.config['SERVER_ROLE'] == 'PROD':
        url="http://backprod.borisreturns.com/pedidos"

  headers = {
    'Content-Type': 'application/json'
  }

  data = {
  "orden": order.id,
  "orden_nro": order.order_number,
  "orden_fecha": str(order.timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")),
  "orden_medio_de_pago": order.metodo_de_pago,
  "orden_tarjeta_de_pago": order.tarjeta_de_pago,
  "orden_gastos_cupon": order.gastos_cupon,
  "orden_gastos_gateway": order.gastos_gateway,
  "orden_gastos_shipping_owner": order.gastos_shipping_owner,
  "orden_gastos_shipping_customer": order.gastos_shipping_customer,
  "orden_gastos_promocion": order.gastos_promocion,
  "correo":{
    "correo_metodo_envio": metodo_envio,
    "correo_id": solicitud['id'],
    "correo_status": solicitud['status'],
    "correo_precio": solicitud['price'],
    "correo_precio_formateado": solicitud['priceFormatted'],
    "correo_moneda":solicitud['currency'],
  },
  "cliente": {
    "id": user.id,
    "name": user.name,
    "identification": user.identification,
    "email":user.email,
    "phone":user.phone,
    "address": {
      "street":user.address,
      "number":user.number,
      "floor":user.floor,
      "zipcode":user.zipcode,
      "locality":user.locality,
      "city":user.city,
      "province":user.province,
      "country":user.country
    }
  },
  "company": {
    "id": company.id,
    "platform": company.platform,
    "store_id": company.store_id,
    "name": company.company_name,
    "admin_email": company.admin_email,
    "logo": company.logo,
    "address":{
      "street": company.shipping_address,
      "number": company.shipping_number,
      "floor": company.shipping_floor,
      "city": company.shipping_city,
      "state": company.shipping_province,
      "postalCode": company.shipping_zipcode,
      "country": company.shipping_country
    },
    "contact": {
      "firstName": company.contact_name,
      "email": company.contact_email,
      "phone": company.contact_phone
    },
    "producto": []
  }
  }

  productos_tmp = []
  for i in productos:

    if i.accion == 'devolver':
      if i.promo_descuento != 0:
        precio_final = i.promo_precio_final
      else:
        precio_final = i.price
    else:
        precio_final = 0.0
    
    productos_tmp.append (   
    {
      "id": i.prod_id,
      "name": i.name,
      "variant":i.variant,
      "accion": i.accion,
      "accion_cantidad": i.accion_cantidad,
      "accion_cambiar_por": i.accion_cambiar_por,
      "accion_cambiar_por_desc": i.accion_cambiar_por_desc,
      "monto_a_devolver": precio_final,
      "precio": i.price,
      "promo_descuento": i.promo_descuento,
      "promo_nombre": i.promo_nombre,
      "promo_precio_final": i.promo_precio_final,
      "motivo": i.motivo
    }
    )

  data['producto'] = productos_tmp
  
  if 'test' in session:  
    if session['test'] == 'True':
      with open(url, "w") as outfile:
        json.dump(data, outfile)
    else:     
      solicitud = requests.request("POST", url, headers=headers, data=json.dumps(data))
      if solicitud.status_code != 200:
        flash('Hubo un problema con la generación del pedido. Error {}'.format(solicitud.status_code))
        loguear_error('almacena_envio', 'Hubo un problema con la generación de la orden en Boris', solicitud.status_code, json.dumps(data) )
        return 'Failed'
      else: 
        flash('Se envio el pedido correctamente')
        loguear_error('almacena_envio', 'EL pedido paso correctamente','OK', json.dumps(data) )
        return 'Success'

  
############################## carga_pedido ##################################################
def cargar_pedido(unaEmpresa, pedido ):

  session['store'] = unaEmpresa.store_id
  session['plataforma'] = unaEmpresa.platform

  if Customer.query.get(pedido['customer']['id']):
    unCliente = Customer.query.get(pedido['customer']['id'])
  else: 
    unCliente = Customer(
      id = pedido['customer']['id'],
      name =pedido['customer']['name'],
      identification = pedido['customer']['identification'],
      email = pedido['customer']['email'],
      phone = pedido['customer']['phone'],
      address = pedido['shipping_address']['address'],
      number = pedido['shipping_address']['number'],
      floor = pedido['shipping_address']['floor'],
      zipcode = pedido['shipping_address']['zipcode'],
      locality = pedido['shipping_address']['locality'],
      city = pedido['shipping_address']['city'],
      province = pedido['shipping_address']['province'],
      country = pedido['shipping_address']['country'],
      pertenece = unaEmpresa
      )
  session['cliente'] = unCliente.id

  ## cambio
  if Order.query.get(pedido['id']):
    unaOrden = Order.query.get(pedido['id'])
  else: 
    unaOrden = Order(
      id = pedido['id'],
      order_number = pedido['number'],
      order_original_id = pedido['id'],
      order_fecha_compra = datetime.strptime((pedido['completed_at']['date']), '%Y-%m-%d %H:%M:%S.%f'),
      metodo_de_pago = pedido['gateway'],
      tarjeta_de_pago = pedido['payment_details']['credit_card_company'],
      gastos_cupon = pedido['discount_coupon'],
      gastos_gateway = pedido['discount_gateway'],
      gastos_shipping_owner = pedido['shipping_cost_owner'],
      gastos_shipping_customer = pedido['shipping_cost_customer'],
      gastos_promocion = pedido['promotional_discount']['total_discount_amount'],
      buyer = unCliente
      )
  session['orden'] = unaOrden.id       

  for x in range(len(pedido['products'])): 
    promo_tmp = buscar_promo(pedido['promotional_discount']['contents'], pedido['products'][x]['id'] )
    
    unProducto = Producto(
      id =  pedido['products'][x]['id'],
      prod_id = pedido['products'][x]['product_id'],
      name = pedido['products'][x]['name'],
      price = pedido['products'][x]['price'],
      quantity = pedido['products'][x]['quantity'],
      variant = pedido['products'][x]['variant_id'],
      image = pedido['products'][x]['image']['src'],
      accion = "ninguna",
      motivo =  "",
      politica_valida = validar_politica(unaOrden.order_fecha_compra)[0],
      politica_valida_motivo = validar_politica(unaOrden.order_fecha_compra)[1],
      accion_cantidad = pedido['products'][x]['quantity'],
      promo_precio_final = promo_tmp[2],
      promo_descuento = promo_tmp[1],
      promo_nombre = promo_tmp[0],
      articulos = unaOrden
      )

    db.session.add(unProducto)
  db.session.commit()



############################## buscar_tracking ##################################################
def busca_tracking(orden):
  url = "http://ec2-34-199-104-15.compute-1.amazonaws.com/orden/tracking"
  params = {'orden_id': orden}
  historia = requests.request("GET", url, params=params).json()
  return historia


############################## loguea_error ##################################################
def loguear_error(modulo, mensaje, codigo, texto):
  url = "logs/app/"+str(session['store'])+"_log.txt"
  outfile = open(url, "a+")
  outfile.write(str(datetime.utcnow())+','+ modulo +','+ mensaje +','+ str(codigo) +','+str(texto)+ '\n')
  outfile.close()


############################## valida_politica ##################################################
def validar_politica(orden_fecha):
  
  hoy = datetime.utcnow()
  #### valida ventana de cambios ####
  periodo_cambio = session['ventana_cambio']
  if abs((hoy - orden_fecha).days) > periodo_cambio:
    cambio = "NOK"
  else: 
    cambio = "OK"
  
  #flash('Cambio {} - periodo {} - {}'.format(cambio, periodo_cambio, abs((hoy - orden_fecha).days) ))
  #### valida ventana de devolcuiones ####
  periodo_devolucion = session['ventana_devolucion']
  if abs((hoy - orden_fecha).days) > periodo_devolucion:
    devolucion = "NOK"
  else: 
    devolucion = "OK"
  
  #flash('Devolucion {} - periodo {} - {}'.format(devolucion, periodo_devolucion, abs((hoy - orden_fecha).days) ))
  ### devuelve valor
  if cambio == "OK" and devolucion == "OK":
    resultado_politica = ["Ambos",'']
  else: 
    if cambio == "OK" and devolucion == "NOK":
      resultado_politica =  ["Solo Cambio",' El período para realizar devoluciones expiró ']
    else: 
      if cambio == "NOK" and devolucion == "OK":
        resultado_politica =  ["Solo Devolucion",' El período para realizar cambios expiró ']
      else: 
        if cambio == "NOK" and devolucion == "NOK":
          resultado_politica =  ["Ninguno",' El período para realizar cambios/devoluciones expiró ']

  #flash('resultado {}'.format(resultado_politica)) 
  return resultado_politica
  

def validar_cobertura(provincia,zipcode):
  if provincia in session['provincia_codigos_postales']:
    if session['provincia_codigos_postales'][provincia] == "All":
      return True
    else: 
      for x in range(len(session['provincia_codigos_postales'][provincia])):
        if zipcode == session['provincia_codigos_postales'][provincia][x] or zipcode == str(session['provincia_codigos_postales'][provincia][x]):
          return True
      return False
  else:
    return False
  
### Selecciona el texto a mostrar segun la empresa
def traducir_texto(string, fp):
  file1 = open('app/static/conf/'+fp+'.txt', 'r')
  for line in file1:
    if line.startswith(string):
      return line.split(string,1)[1] 


def actualizar_store(store):
  empresa = Store.query.filter_by(store_id=store['store_id']).first()
  ## Actualiza datos JSON

  ## carga datos nuevos de la empresa en BBDD
  empresa.platform = store['platform']
  empresa.platform_token_type = store['platform_token_type']
  empresa.platform_access_token = store['platform_access_token']
  empresa.store_name = store['store_name']
  empresa.store_url = store['store_url']
  empresa.store_phone = store['store_phone']
  empresa.store_address = store['store_address']
  empresa.admin_email = store['admin_email']
  empresa.communication_email = store['communication_email']
  empresa.param_logo = store['param_logo']
  empresa.param_fondo = store['param_fondo']
  empresa.store_main_language = store['store_main_language']
  empresa.store_main_currency = store['store_main_currency']
  empresa.store_country = store['store_country']
  empresa.correo_test = store['correo_test']
  empresa.correo_usado = store['correo_usado']
  empresa.correo_apikey = store['correo_apikey']
  empresa.correo_id = store['correo_id']
  empresa.contact_email = store['contact_email']
  empresa.contact_name = store['contact_name']
  empresa.contact_email = store['contact_email']
  empresa.contact_phone = store['contact_phone'] 
  empresa.shipping_address = store['shipping_address']
  empresa.shipping_number = store['shipping_number']
  empresa.shipping_floor = store['shipping_floor']
  empresa.shipping_zipcode = store['shipping_zipcode']
  empresa.shipping_city = store['shipping_city']
  empresa.shipping_province = store['shipping_province']
  empresa.shipping_country = store['shipping_country']
  empresa.shipping_info = store['shipping_info']

  db.session.commit()
  return 'Success'


def crear_store(store):

  ################################ Crea JSON de Configuración ########################################
  ################################ Datos por defecto de Inicio ###########################################
  if current_app.config['SERVER_ROLE'] == 'DEV':
    conf_url='app/static/conf/'+store['store_id']+'.json'
  if current_app.config['SERVER_ROLE'] == 'PROD':
    conf_url='app/static/conf/'+store['store_id']+'.json'
    
  conf_file = {
    "currency": store['store_main_currency'],
    "shipping": "customer",
    "test": "False",
    "correo_test": "True",
    "envio": ["manual", "retiro", "coordinar"],
    "provincia_codigos_postales": {
      "Capital Federal":"All",
      "Buenos Aires": [1636, 1637, 1638, 1602, 1605, 1606]
    },
    "motivos":[
      "No calza bien",
      "Es grande",
      "Es chico",
      "Mala calidad",
      "No gusta color"
    ],
    "politica": {
      "ventana_cambio":30,
      "ventana_devolucion":30,
      "rubros":{},
      "promos":{}
    },
    "textos": {
      "elegir_opcion_cambio": "Seleccioná la opción que queres o elegi generar un cupín si querés cambiarlo por otra cosa",
      "elegir_opcion_cambio_cupon": "Seleccioná esta opción para obtener un cupón de crédito en nuestra tienda ",
      "elegir_accion": "Selecciona la acción a realizar",
      "envio_manual": "Seleccionaste envío manual",
      "boton_envio_manual": "Traer la orden a nuestro local",
      "boton_envio_manual_desc": "Acercanos el/los productos a nuestros locales/depósito",
      "boton_envio_retiro": "Retirar en tu domicilio",
      "boton_envio_retiro_desc": "Un servicio de correo pasara a buscar los productos por tu domicilio",
      "boton_envio_coordinar": "Coordinar método de retiro",
      "boton_envio_coordinar_desc": "Coordina con nosotros el metodo de envio que te quede mas cómodo"
    }
  }
  with open(conf_url, "w+") as outfile:
    json.dump(conf_file, outfile)

  ################################ Crea el Store en la BBD ########################################
  unStore = Store(
    ## datos solo para la creación
    store_id = store['store_id'],
    param_config = conf_url,
    ## Otros datos
    platform = store['platform'],
    platform_token_type = store['platform_token_type'],
    platform_access_token = store['platform_access_token'],
    store_name = store['store_name'],
    store_url = store['store_url'],
    store_phone = store['store_phone'],
    store_address = store['store_address'],
    admin_email = store['admin_email'],
    contact_email = store['contact_email'],
    param_logo = store['param_logo'],
    store_main_language = store['store_main_language'],
    store_main_currency = store['store_main_currency'],
    store_country = store['store_country'],
    correo_test = store['correo_test']
  )
  db.session.add(unStore)
  db.session.commit()
  return 'Success'