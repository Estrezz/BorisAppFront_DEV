
import requests
import json
import datetime
import smtplib
import uuid
from os.path import exists
from datetime import datetime
from app import db
from app.models import Customer, Order, Producto, Company
from flask import session, flash, current_app, render_template
# from app.main.moova import crea_envio_moova, cotiza_envio_moova
from app.main.tiendanube import buscar_pedido_tiendanube, buscar_producto_nombre_tiendanube, cargar_pedido_tiendanube, buscar_pedido_conNro_tiendanube, buscar_alternativas_tiendanube, validar_categorias_tiendanube, buscar_producto_tiendanube, agregar_nota_tiendanube
from app.main.shopify import buscar_pedido_shopify, cargar_pedido_shopify, buscar_alternativas_shopify, buscar_producto_shopify, buscar_producto_nombre_shopify
from app.email import send_email


def buscar_nro_pedido(lista, valor):
    for x in lista:
     if x['number'] == valor:
          return x
    else:
     return 'None'


def buscar_pedido(empresa, ordernum, ordermail):

  ################## TiendaNube ##############################
  if empresa.platform == 'tiendanube':
    order = buscar_pedido_tiendanube(empresa, ordermail, int(ordernum))
       
    if order == "REINTENTAR" :
      return 'Reintentar'
    if  order == "TIMEOUT" :  
      return 'Timeout'
    if  order == "NOTFOUND" :
      return 'Notfound'  

  ################## Shopify ##############################
  if empresa.platform == 'shopify':
    order = buscar_pedido_shopify(empresa, ordernum, ordermail)
  
  return order


def buscar_pedido_conNro(empresa, orderid):
  if empresa.platform == 'tiendanube':
    order = buscar_pedido_conNro_tiendanube(empresa, orderid)
   
  return order

###### Busca el nombre del Producto
def buscar_producto_nombre(company, storeid, prod_id, item_variant):

  ### Para Tiendanube
  if company.platform == 'tiendanube':
    name = buscar_producto_nombre_tiendanube(company, storeid, prod_id)
  
  ### Para Shopify
  if company.platform == 'shopify':
    name = buscar_producto_nombre_shopify(company, storeid, prod_id)

  # Si el producto no existe (fue eliminado despues de la compra)
  if name == 404:
    return ('', [])

  return name

#####################################################################################################
# Busca alternativas para cambiar un articulo según el motivo de cambio
# devuelve lista con productos alternativos y le oden de los atributos (para tener como encabezados)
#####################################################################################################
def buscar_alternativas(company, storeid, prod_id, item_variant):
  
  if company.platform == 'tiendanube':
    alternatives = buscar_alternativas_tiendanube(company, storeid, prod_id, item_variant)

  if company.platform == 'shopify':
    alternatives = buscar_alternativas_shopify(company, storeid, prod_id, item_variant)

    #### Si el producto fue eliminado luego de la compra #####
  if alternatives == 404:
    return ('', [])
    
  return alternatives    
  


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

    if current_app.config['SERVER_ROLE'] == 'PREDEV':
      url='https://devback.borisreturns.com/datos_empresa'
    if current_app.config['SERVER_ROLE'] == 'DEV':
      url='https://back.borisreturns.com/datos_empresa'
    if current_app.config['SERVER_ROLE'] == 'PROD':
      url='https://backprod.borisreturns.com/datos_empresa'
    params = {'store_id': empresa}
    empresa_tmp = requests.request("GET", url, params=params)

    try:
        empresa_tmp = empresa_tmp.json()
    except json.JSONDecodeError:
        return "Failed"
    
     
    ### Setea el nombre del SENDER en el mail saliente - SI no lo tiene configurado
    ### toma la parte anterior al @
    if 'communication_email_name' in empresa_tmp.keys():
      communication_email_name_tmp = empresa_tmp['communication_email_name']
    else:
      communication_email_name_tmp =  empresa_tmp['communication_email'].split("@")[0]

    unaEmpresa = Company(
      platform = empresa_tmp['platform'],
      store_id = empresa_tmp['store_id'],
      platform_token_type = empresa_tmp['platform_token_type'],
      platform_access_token = empresa_tmp['platform_access_token'],
      company_name = empresa_tmp['company_name'],
      company_url = empresa_tmp['company_url'],
      company_country = empresa_tmp['company_country'],
      company_main_language = empresa_tmp['company_main_language'],
      company_main_currency = empresa_tmp['company_main_currency'],
      admin_email = empresa_tmp['admin_email'],
      communication_email = empresa_tmp['communication_email'],
      communication_email_name = communication_email_name_tmp,
      logo = empresa_tmp['param_logo'],
      fondo = empresa_tmp['param_fondo'],
      correo_usado = empresa_tmp['correo_usado'],
      correo_apikey = empresa_tmp['correo_apikey'],
      correo_id = empresa_tmp['correo_id'],
      correo_test = empresa_tmp['correo_test'],
      correo_apikey_test = empresa_tmp['correo_apikey_test'],
      correo_id_test = empresa_tmp['correo_id_test'],
      contact_name = empresa_tmp['contact_name'],
      contact_email = empresa_tmp['contact_email'],
      contact_phone = empresa_tmp['contact_phone'],
      shipping_address = empresa_tmp['shipping_address'],
      shipping_number = empresa_tmp['shipping_number'],
      shipping_floor = empresa_tmp['shipping_floor'],
      shipping_zipcode = empresa_tmp['shipping_zipcode'],
      shipping_city = empresa_tmp['shipping_city'],
      shipping_province = empresa_tmp['shipping_province'],
      shipping_country = empresa_tmp['shipping_country'],
      shipping_info = empresa_tmp['shipping_info']
    )
    
    #### guarda settings de la empresa
    settings = guardar_settings(empresa)
    session['shipping'] = settings['shipping']
    session['test'] = settings['test']
    session['correo_test'] = settings['correo_test']
    session['provincia_codigos_postales'] = settings['provincia_codigos_postales']
    session['ventana_cambio'] = settings['politica']['ventana_cambio']
    session['ventana_devolucion'] = settings['politica']['ventana_devolucion']
    session['textos'] = settings['textos']
    session['envio'] = settings['envio']
    session['motivos'] = settings['motivos']
    
    if 'cupon' in settings.keys():
      session['cupon'] = settings['cupon']
    else: 
      session['cupon'] = 'Si'
    
    if 'otracosa' in settings.keys():
      session['otracosa'] = settings['otracosa']
    else: 
      session['otracosa'] = 'No'
    
    if 'observaciones' in settings.keys():
      session['observaciones'] = settings['observaciones']
    else: 
      session['observaciones'] = 'No'
    
    session['rubros'] = settings['politica']['rubros']

    ### Multiplataforma #####################################
    if empresa_tmp['platform'] == "tiendanube": 
      session['ids_filtrados'] = validar_categorias_tiendanube(unaEmpresa)
    ###### ver Shopify ##########################33
    else: 
      session['ids_filtrados'] = []
     
  else: 
    settings = guardar_settings('1447373')
    session['shipping'] = settings['shipping']
    session['test'] = settings['test']
    session['correo_test'] = settings['correo_test']
    session['provincia_codigos_postales'] = settings['provincia_codigos_postales']
    session['ventana_cambio'] = settings['politica']['ventana_cambio']
    session['ventana_devolucion'] = settings['politica']['ventana_devolucion']
    session['textos'] = settings['textos']
    session['envio'] = settings['envio']
    session['motivos'] = settings['motivos']
    session['rubros'] = settings['politica']['rubros']
    if 'cupon' in settings.keys():
      session['cupon'] = settings['cupon']
    else: 
      session['cupon'] = 'Si'
    session['ids_filtrados'] = []
    
    if 'otracosa' in settings.keys():
      session['otracosa'] = settings['otracosa']
    else: 
      session['otracosa'] = 'No'

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
      logo = 'https://frontprod.borisreturns.com/static/images/BorisReturns.png',
      fondo = '/static/images/Boris_back.png',
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
def guardar_settings(store_id):
  url = 'app/static/conf/'+str(store_id)+'.json'
  with open(url, encoding='utf-8') as json_file:
    data = json.load(json_file)
    return data


############################## crea_envio ##################################################
def crea_envio(company, user, order, productos, metodo_envio): 
  solicitud_envio = {
        "id": metodo_envio['correo_id'],
        "status":'DRAFT',
        "price": metodo_envio['precio_envio'],
        "priceFormatted":'0.0',
        "currency":'ARS'
  }
    
  mandaBoris = almacena_envio(company, user, order, productos, solicitud_envio, metodo_envio)
  if mandaBoris != 'Failed':
    try:
      send_email(session['textos']['orden_solicitada_asunto'], 
                sender=(company.communication_email_name, company.communication_email),
                recipients=[user.email], 
                reply_to = company.admin_email,
                text_body=render_template('email/pedido_listo.txt',
                                         user=user, company=company, productos=productos, envio=solicitud_envio, order=order, shipping=session['shipping'], metodo_envio=metodo_envio['metodo_envio_id'], textos=session['textos']),
                html_body=render_template('email/pedido_listo.html',
                                         user=user, company=company, productos=productos, envio=solicitud_envio, order=order, shipping=session['shipping'], metodo_envio=metodo_envio['metodo_envio_id'], textos=session['textos']), 
                attachments=None,
                sync=False,
                bcc=[current_app.config['ADMINS'][0]])
                
    except smtplib.SMTPException as e:
      error_mail = e
      flash('Mensaje {}'.format('a.error_mail'))

    send_email('Se ha generado una orden en Boris', 
                sender=(company.communication_email_name, company.communication_email),
                recipients=[company.admin_email], 
                reply_to = company.admin_email,
                text_body=render_template('email/nuevo_pedido.txt',
                                         user=user, envio=solicitud_envio, order=order, shipping=session['shipping']),
                html_body=render_template('email/nuevo_pedido.html',
                                         user=user, envio=solicitud_envio, order=order, shipping=session['shipping']), 
                attachments=None, 
                sync=False,
                bcc=[])
  return solicitud_envio


################################################
#### Cotizar el precio del envío               #
################################################
def cotiza_envio(company, user, order, productos, correo):
  
  if current_app.config['SERVER_ROLE'] == 'PREDEV':
    url='https://devback.borisreturns.com/cotiza_envio'
  if current_app.config['SERVER_ROLE'] == 'DEV':
    url="https://back.borisreturns.com/cotiza_envio"
  if current_app.config['SERVER_ROLE'] == 'PROD':
    url="https://backprod.borisreturns.com/cotiza_envio"

  headers = {
    'Content-Type': 'application/json'
  }

  data = {
    "correo":{
      "correo_id": correo['correo_id'],
      "store_id": company.store_id,
      "metodo_envio": correo['metodo_envio_id'],
      #### Salientes identifica si hay articulos que deben enviarse al cliente
      "salientes":order.salientes,
      "orden_nro": order.order_number
    },
    "from": {
        "street": user.address,
        "number": user.number,
        "floor": user.floor,
        "city": user.city,
        "state": user.province,
        "postalCode": user.zipcode,
        "country": user.country,
        "contact": {
          "firstName": user.name,
          "email": user.email
        }
    },
    "to": {
        "street": company.shipping_address,
        "number": company.shipping_number,
        "floor": company.shipping_floor,
        "city": company.shipping_city,
        "state": company.shipping_province,
        "postalCode": company.shipping_zipcode,
        "country": company.shipping_country,
        "contact": {
          "firstName": company.contact_name,
          "email": company.contact_email,
          "phone": company.contact_phone
        }
      },
  }

  items_envio = []
  for i in productos:
    items_envio.append (   
      {
        "descripcion": i.name,
        "precio": i.price,
        "cantidad": i.accion_cantidad,
        "alto":i.alto,
        "largo": i.largo,
        "profundidad" : i.profundidad,
        "peso": i.peso
      }
    )

  data['items'] = items_envio

  solicitud = requests.request("POST", url, headers=headers, data=json.dumps(data))
  #flash(json.dumps(data))
  if solicitud.status_code != 200:
    #flash('Error al cotizar {} - {}'.format(solicitud.status_code, solicitud.content))
    return 'Failed'
  else: 
    solicitud = solicitud.json()
    return solicitud
    

############################## almacena_envio ##################################################
def almacena_envio(company, user, order, productos, solicitud, metodo_envio):
  if 'test' in session:  
    if session['test'] == 'True':
      url='../Boris_common/logs/pedido'+str(order.id)+'.json'
    else: 
      if current_app.config['SERVER_ROLE'] == 'PREDEV':
        url='https://devback.borisreturns.com/pedidos'
      if current_app.config['SERVER_ROLE'] == 'DEV':
        url="https://back.borisreturns.com/pedidos"
      if current_app.config['SERVER_ROLE'] == 'PROD':
        url="https://backprod.borisreturns.com/pedidos"

  headers = {
    'Content-Type': 'application/json'
  }

  data = {
  "orden": order.id,
  "orden_nro": order.order_number,
  "orden_fecha": str(order.timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")),
  "orden_medio_de_pago": order.metodo_de_pago,
  "order_salientes": order.salientes,
  "orden_tarjeta_de_pago": order.tarjeta_de_pago,
  "orden_gastos_cupon": order.gastos_cupon,
  "orden_gastos_gateway": order.gastos_gateway,
  "orden_gastos_shipping_owner": order.gastos_shipping_owner,
  "orden_gastos_shipping_customer": order.gastos_shipping_customer,
  "orden_gastos_promocion": order.gastos_promocion,
  "correo":{
    "correo_metodo_envio": metodo_envio['metodo_envio_id'],
    "correo_id": solicitud['id'],
    "correo_status": solicitud['status'],
    "correo_precio": solicitud['price'],
    "correo_precio_formateado": solicitud['priceFormatted'],
    "correo_moneda":solicitud['currency'],
    "metodo_envio_sucursal": order.metodo_envio_sucursal,
    "metodo_envio_sucursal_name": order.metodo_envio_sucursal_name
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
      "accion_cambiar_por_prod_id": i.accion_cambiar_por_prod_id,
      "accion_cambiar_por_desc": i.accion_cambiar_por_desc,
      "monto_a_devolver": precio_final,
      "precio": i.price,
      "alto":i.alto,
      "largo": i.largo,
      "profundidad" : i.profundidad,
      "peso": i.peso,
      "promo_descuento": i.promo_descuento,
      "promo_nombre": i.promo_nombre,
      "promo_precio_final": i.promo_precio_final,
      "motivo": i.motivo,
      "observaciones": i.observaciones
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
        if solicitud.status_code == 409:
          
          respuesta_tmp = solicitud.content
          respuesta = respuesta_tmp.decode("utf-8")

          if respuesta == 'Cambia metodo':
            mensaje = 'El cliente está intentando cambiar el método de envío'
          if respuesta == 'Cambio de accion':
            mensaje = 'El cliente está intentando cambiar su decisión inicial'
          if respuesta == 'Cambio de producto':
            mensaje = 'El cliente está intentando cambiar el producto seleccionado inicialmente'
          if respuesta == 'Agrega / quita artículos':
            mensaje = 'El cliente está intentando agregar o quitar un producto'
          if respuesta == 'Solicitud duplicada':
            mensaje = 'Las solicitudes parecen iguales'

          flash('Ya existe una solicitud para esa orden. Error {} - {}'.format(solicitud.status_code, mensaje))
          loguear_error('almacena_envio', 'Ya existe una solicitud', solicitud.status_code, json.dumps(data) )
        else:
          respuesta_tmp = solicitud.content
          respuesta = respuesta_tmp.decode("utf-8")
          mensaje = 'Hubo un error en la generacion del pedido'
          flash('Hubo un problema con la generación del pedido. Error {}'.format(solicitud.status_code))
          loguear_error('almacena_envio', 'Hubo un problema con la generación de la orden en Boris', solicitud.status_code, json.dumps(data) )

        
        send_email('ERROR en creación solicitud ', 
                    sender=current_app.config['ADMINS'][0],
                    recipients=[company.admin_email], 
                    reply_to = current_app.config['ADMINS'][0],
                    text_body=render_template('email/error_solicitud_cliente.txt',
                                            user=user, data=mensaje, order=order, company=company),
                    html_body=render_template('email/error_solicitud_cliente.html',
                                            user=user, data=mensaje, order=order, company=company), 
                    attachments=None, 
                    sync=False,
                    bcc=[current_app.config['ADMINS'][0]])
          
        return 'Failed'
      else: 
        flash('Se envio el pedido correctamente')
        loguear_error('almacena_envio', 'EL pedido paso correctamente','OK', json.dumps(data) )
        return 'Success'

  
############################## carga_pedido ##################################################
def cargar_pedido(unaEmpresa, pedido ):

  session['uid'] = uuid.uuid4()
  session['store'] = unaEmpresa.store_id
  session['plataforma'] = unaEmpresa.platform

  if unaEmpresa.platform == 'tiendanube':
    cargar_pedido_tiendanube(unaEmpresa, pedido )
  if unaEmpresa.platform == 'shopify':
    cargar_pedido_shopify(unaEmpresa, pedido )
  
  return "OK"




############################## buscar_tracking ##################################################
def busca_tracking(orden):
  if current_app.config['SERVER_ROLE'] == 'PREDEV':
    url='http://devback.borisreturns.com/orden/tracking'
  if current_app.config['SERVER_ROLE'] == 'DEV':
    url='http://back.borisreturns.com/orden/tracking'
  if current_app.config['SERVER_ROLE'] == 'PROD':
    url='http://backprod.borisreturns.com/orden/tracking'
  params = {'orden_id': orden}
  historia = requests.request("GET", url, params=params)
  if historia.status_code != 200:
        historia = {}
  else:
        historia = historia.json()
  return historia


############################## loguea_error ##################################################
def loguear_error(modulo, mensaje, codigo, texto):
  if 'store' in session:
        url = "logs/app/" + str(session['store']) + "_log.txt"
  else:
        url = "logs/app/unknown_store_log.txt"
  #url = "logs/app/"+str(session['store'])+"_log.txt"
  outfile = open(url, "a+")
  outfile.write(str(datetime.utcnow())+','+ modulo +','+ mensaje +','+ str(codigo) +','+str(texto)+ '\n')
  outfile.close()





def validar_cobertura(provincia,zipcode):

  if zipcode.isdigit():
    if int(zipcode) < 1900:
      return True
  return False
  
### Selecciona el texto a mostrar segun la empresa
def traducir_texto(string, fp):
  file1 = open('app/static/conf/'+fp+'.txt', 'r')
  for line in file1:
    if line.startswith(string):
      return line.split(string,1)[1] 



def crear_store(store):
  ################################ Crea JSON de Configuración ########################################
  ################################ Datos por defecto de Inicio ###########################################
  if current_app.config['SERVER_ROLE'] == 'DEV':
    conf_url='app/static/conf/'+store['store_id']+'.json'
  if current_app.config['SERVER_ROLE'] == 'PROD':
    conf_url='app/static/conf/'+store['store_id']+'.json'

  ### verficar si existe el archivo ####
  if exists(conf_url):
    return 'Failed'
  
  conf_file = {
    "currency": store['store_main_currency'],
    "shipping": "customer",
    "test": "False",
    "correo_test": "True",
    "envio": [{
            "metodo_envio_id": "Coordinar",
            "icon": "bi bi-headphones",
            "boton_titulo": "Coordinar método de retiro",
            "boton_descripcion": "Coordiná con nosotros el método de envío que te quede mas cómodo",
            "direccion_obligatoria": True,
            "carrier": False,
            "correo_id": "",
            "costo_envio": "Merchant"
        }, {
            "metodo_envio_id": "Manual",
            "icon": "bi bi-handbag",
            "boton_titulo": "Traer la orden a nuestro local",
            "boton_descripcion": "Acercanos el/los productos a nuestros locales/depósito",
            "direccion_obligatoria": False,
            "carrier": False,
            "correo_id": "",
            "costo_envio": "Merchant"
        }
    ],
    "provincia_codigos_postales": {
      "Capital Federal":"All",
      "Buenos Aires": [1636, 1637, 1638, 1602, 1605, 1606]
    },
    "motivos":[
      "No calza bien",
      "Es grande",
      "Es chico",
      "Mala calidad",
      "No gusta color",
      "No es lo que esperaba"
    ],
    "politica": {
      "ventana_cambio":30,
      "ventana_devolucion":30,
      "rubros":{},
      "promos":{}
    },
    "cupon": "No",
    "otracosa": "Si",
    "textos": {
      "elegir_opcion_cambio": "Seleccioná si queres cambiarlo por una variante del mismo articulo o elegí otro producto",
      "elegir_opcion_cambio_cupon": "Seleccioná esta opción para obtener un cupón de crédito en nuestra tienda ",
      "elegir_opcion_otra_cosa": "Elegí en nuestra tienda el artículo que querés, ingresa el nombre y presion buscar",
      "elegir_accion": "Seleccioná la acción a realizar",
      "envio_manual": "Seleccionaste envío manual",
      "boton_envio_manual": "Traer la orden a nuestro local",
      "boton_envio_manual_desc": "Acercanos el/los productos a nuestros locales/depósito",
      "boton_envio_retiro": "Retirar en tu domicilio",
      "boton_envio_retiro_desc": "Un servicio de correo pasara a buscar los productos por tu domicilio",
      "boton_envio_coordinar": "Coordinar método de retiro",
      "boton_envio_coordinar_desc": "Coordiná con nosotros el método de envío que te quede mas cómodo",
      "orden_solicitada_asunto": "Tu orden ha sido iniciada",
      "portal_empresa": store['store_name'],
      "portal_titulo": "Cambios y Devoluciones",
      "portal_texto": "",
    }
  }
  with open(conf_url, "w+") as outfile:
    json.dump(conf_file, outfile)

  return 'Success'


def actualiza_json_categoria(archivo_config, data):
        with open(archivo_config, encoding='utf-8') as json_file:
                json_decoded = json.load(json_file)

        json_decoded['politica']['rubros'] = data['categorias']

        with open(archivo_config, 'w', encoding='utf8') as json_file:
            json.dump(json_decoded, json_file)
  
        return 'Success'


def actualiza_json(archivo_config, clave, data, key):
        with open(archivo_config, encoding='utf-8') as json_file:
          json_decoded = json.load(json_file)

          if (key=='textos' or key=='politica' or key=='provincia_codigos_postales'):
            json_decoded[key][clave] = data[clave]

          if key=='otros':
            json_decoded[clave] = data[clave]

        with open(archivo_config, 'w', encoding='utf8' ) as json_file:
            json.dump(json_decoded, json_file)

        return 'Success'



def buscar_producto(empresa, desc_prod):     
  if empresa.platform == 'tiendanube':
    product = buscar_producto_tiendanube(empresa, desc_prod)
  
  if empresa.platform == 'shopify':
    product = buscar_producto_shopify(empresa, desc_prod)

  return product


def agregar_nota(company, order):
    if company.platform == 'tiendanube':
      agregar_nota_tiendanube(company, order)
      return
    else:
      return

############################## buscar_empresa ##################################################
def buscar_sucursales(empresa):
  ##sucursal = http://127.0.0.1:5000/api/sucursales/listar?tienda=1447373&metodo_envio=Locales
  
  if current_app.config['SERVER_ROLE'] == 'PREDEV':
    url=f"https://devback.borisreturns.com/api/sucursales/listar?tienda={empresa}&metodo_envio=Locales"
  if current_app.config['SERVER_ROLE'] == 'DEV':
    url=f"http://back.borisreturns.com/api/sucursales/listar?tienda={empresa}&metodo_envio=Locales"
  if current_app.config['SERVER_ROLE'] == 'PROD':
    url=f"http://backprod.borisreturns.com/api/sucursales/listar?tienda={empresa}&metodo_envio=Locales"

  sucursales_tmp = requests.request("GET", url)

  if sucursales_tmp.status_code != 200:
        sucursales_list = [{"sucursal_name": "No se encontró ninguna sucursal"}]
  else:
        sucursales = sucursales_tmp.json()
        sucursales_list = [{"sucursal_id":s['sucursal_id'],"sucursal_name":s['sucursal_name'],"sucursal_direccion":s['sucursal_direccion'],"sucursal_observaciones":s['sucursal_observaciones']} for s in sucursales ]

  return sucursales_list

     