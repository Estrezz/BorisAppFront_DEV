import requests
import json
import datetime
from datetime import datetime
from app import db
from app.models import Customer, Order, Producto, Company, Store
from flask import session, flash, current_app, render_template
from app.main.moova import crea_envio_moova, cotiza_envio_moova
from app.email import send_email


def buscar_nro_pedido(lista, valor):
    for x in lista:
     if x['number'] == valor:
          return x
    else:
     return 'None'


def buscar_pedido(empresa, form):
  if empresa.platform == 'tiendanube':
    buscar_pedido_tiendanube(empresa, form)
    url = "https://api.tiendanube.com/v1/"+str(empresa.store_id)+"/orders?q="+form.ordermail.data    
    payload={}
    headers = {
        'Content-Type': 'application/json',
        'Authentication': empresa.platform_token_type+' '+empresa.platform_access_token
    }
    order_tmp = requests.request("GET", url, headers=headers, data=payload).json()

  if type(order_tmp) == dict:
    return 'None'
  else:
    order = buscar_nro_pedido(order_tmp, form.ordernum.data)
    return order


def buscar_pedido_conNro(storeid, orderid):
  url = "https://api.tiendanube.com/v1/"+str(storeid)+"/orders/"+orderid
  
  payload={}
  headers = {
    'User-Agent': 'Boris (erezzonico@borisreturns.com)',
    'Content-Type': 'application/json',
    'Authentication': 'bearer cb9d4e17f8f0c7d3c0b0df4e30bcb2b036399e16'
   }
  order = requests.request("GET", url, headers=headers, data=payload).json()
  
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
def buscar_alternativas(storeid, prod_id, motivo, item_variant):
  url = "https://api.tiendanube.com/v1/"+str(storeid)+"/products/"+str(prod_id)
  
  payload={}
  headers = {
    'User-Agent': 'Boris (erezzonico@borisreturns.com)',
    'Content-Type': 'application/json',
    'Authentication': 'bearer cb9d4e17f8f0c7d3c0b0df4e30bcb2b036399e16'
   }
  product = requests.request("GET", url, headers=headers, data=payload).json()
  variantes = []

  for x in product['variants']:
    # validar stock infinito (NoneType) y permitir cambiar por lo mismo
    # if x['stock'] > 1 and x['id'] != item_variant :
    if isinstance(x['stock'], type(None)) == True:
      variantes.append(x)
    else: 
      if x['stock'] > 1 :
        variantes.append(x)

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
    session['periodo'] = settings['politica']['periodo']
    session['correo_test'] = settings['correo_test']

    unaEmpresa = Company(
      platform = empresa_tmp.platform,
      store_id = empresa_tmp.store_id,
      platform_token_type = empresa_tmp.platform_token_type,
      platform_access_token = empresa_tmp.platform_access_token,
      company_name = empresa_tmp.store_name,
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
    session['periodo'] = settings['politica']['periodo']
    session['correo_test'] = settings['correo_test']

    unaEmpresa = Company(
      platform = 'tiendanube',
      platform_access_token = 'cb9d4e17f8f0c7d3c0b0df4e30bcb2b036399e16',
      platform_token_type = 'bearer',
      store_id = '1447373',
      company_country = 'AR',
      company_main_language = 'es',
      company_main_currency = 'ARS',
      communication_email = 'soporte@borisreturns.com',
      company_name = 'Boris sin Tienda',
      admin_email = 'admin@borisreturns.com',
      logo = '/static/images/Boris_Naranja.png',
      correo_usado = 'Moova',
      correo_apikey = 'b23920003684e781d87e7e5b615335ad254bdebc',
      correo_id = 'b22bc380-439f-11eb-8002-a5572ae156e7',
      correo_test = True,
      correo_apikey_test = 'b23920003684e781d87e7e5b615335ad254bdebc',
      correo_id_test = 'b22bc380-439f-11eb-8002-a5572ae156e7',
      contact_name = 'Pepito Perez',
      contact_email = 'pepito@borisreturns.com',
      contact_phone = '+5491151064817',
      shipping_address = 'Virrey Loreto',
      shipping_number = '2259',
      shipping_floor = '',
      shipping_zipcode = '1426',
      shipping_city = 'CABA',
      shipping_province = 'CABA',
      shipping_country = 'AR',
      shipping_info = 'Entregar a pepito'
    )
  return unaEmpresa


################################# guardar_settings ##########################################
##################### Carga el archivo de settings desde el campo param_config ##############
############################## de la base de empresas #######################################
def guardar_settings(url):
  with open(url) as json_file:
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
      send_email('Tu Orden ha sido confirmada', 
                sender=current_app.config['ADMINS'][0], 
                recipients=[user.email], 
                text_body=render_template('email/1447373/pedido_listo.txt',
                                         user=user, envio=solicitud_envio, order=order, shipping=session['shipping']),
                html_body=render_template('email/1447373/pedido_listo.html',
                                         user=user, envio=solicitud_envio, order=order, shipping=session['shipping']), 
                attachments=None, 
                sync=False)
    except smtplib.SMTPException as e:
      error_mail = e
      flash('Mensaje {}'.format('a.error_mail'))
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



############################## almacena_envio ##################################################
def almacena_envio(company, user, order, productos, solicitud, metodo_envio):
  if 'test' in session:  
    if session['test'] == 'True':
      url='../Boris_common/logs/pedido'+str(order.id)+'.json'
    else: 
      url="http://back.borisreturns.com/pedidos"

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
      valido = validar_politica(unaOrden.order_fecha_compra)[0],
      valido_motivo = validar_politica(unaOrden.order_fecha_compra)[1],
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
  url = "app/logs/"+str(session['store'])+"_log.txt"
  #outfile = open('app/logs/err_boris.txt', "a")
  outfile = open(url, "a+")
  outfile.write(str(datetime.utcnow())+','+ modulo +','+ mensaje +','+ str(codigo) +','+str(texto)+ '\n')
  outfile.close()


############################## valida_politica ##################################################
def validar_politica(orden_fecha):
  
  hoy = datetime.utcnow()
  if 'periodo' in session:  
    periodo = session['periodo']
  else:
    periodo = 30

  if abs((hoy - orden_fecha).days) > periodo:

    #periodo_valido = False
    return [False,'El período para realizar cambios expiró']
  else: 
    #periodo_valido = True
    return [True,'OK']
  

  
