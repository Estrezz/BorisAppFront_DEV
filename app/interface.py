import requests
import json
import datetime
from datetime import datetime
from app import db
from app.models import Customer, Order, Producto, Company, Store
from flask import session, flash

#import os

from app import app


def buscar_nro_pedido(lista, valor):
    for x in lista:
     if x['number'] == valor:
          return x
    else:
     return 'None'


def buscar_pedido(storeid, form):
  url = "https://api.tiendanube.com/v1/"+str(storeid)+"/orders?q="+form.ordermail.data    
  payload={}
  headers = {
    'User-Agent': 'Boris (erezzonico@borisreturns.com)',
    'Content-Type': 'application/json',
    'Authentication': 'bearer cb9d4e17f8f0c7d3c0b0df4e30bcb2b036399e16'
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
    if x['stock'] > 1 and x['id'] != item_variant :
      variantes.append(x)

  devolver = [variantes, product['attributes']]
  return devolver


## Arma string con las descripcion de las variantes
def describir_variante(values):
  desc = ''
  for i in values:
    if desc != '':
      desc = desc + ' - '
    desc = desc + i['es'] 
  return desc

def buscar_empresa(empresa):
  if empresa != 'Ninguna':
    empresa_tmp = Store.query.filter(Store.store_id == empresa).first()
    #### guarda settings de la empresa
    settings = guardar_settings(empresa_tmp.param_config)
    session['paga_correo'] = settings['shipping']
    session['test'] = settings['test']
    session['periodo'] = settings['politica']['periodo']

    unaEmpresa = Company(
      platform = empresa_tmp.platform,
      store_id = empresa_tmp.store_id,
      company_name = empresa_tmp.store_name,
      admin_email = empresa_tmp.admin_email,
      logo = empresa_tmp.param_logo,
      correo_usado = empresa_tmp.correo_usado,
      correo_apikey = empresa_tmp.correo_apikey,
      correo_id = empresa_tmp.correo_id,
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
    session['paga_correo'] = settings['shipping']
    session['test'] = settings['test']
    session['periodo'] = settings['politica']['periodo']
    unaEmpresa = Company(
      platform = 'TiendaNube',
      store_id = '1447373',
      company_name = 'Boris sin Tienda',
      admin_email = 'admin@borisreturns.com',
      logo = '/static/images/Boris_Naranja.png',
      correo_usado = 'Moova',
      correo_apikey = 'b23920003684e781d87e7e5b615335ad254bdebc',
      correo_id = 'b22bc380-439f-11eb-8002-a5572ae156e7',
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


######## Carga el archivo de settings desde el campo param_config ########
############ de la base de empresas ######################################
def guardar_settings(url):
  with open(url) as json_file:
    data = json.load(json_file)
    return data


def crea_envio(company, user, order, productos):
  url = "https://api-dev.moova.io/b2b/shippings"
  headers = {
    'Authorization': company.correo_apikey,
    'Content-Type': 'application/json',
   }
  params = {'appId': company.correo_id}

  if 'paga_correo' in session:  
    if session['paga_correo'] == 'customer':
      paga_correo = 'manual'
    else: 
      paga_correo ='semi-automatic'
  else:
    paga_correo ='semi-automatic'

  solicitud_tmp = {
  "currency": "ARS",
  "type": "regular",
  "flow": paga_correo,
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
    },
    "message": ""
  },
  "internalCode": order.id,
  "extra": {},
  "conf": {
    "assurance": False,
    "items": [
    ]
  }
}

  items_envio = []
  for i in productos:
    items_envio.append (   
    {
        "item": {
          "description": i.name,
          "price": i.price,
          "quantity": i.accion_cantidad
        }
      }
    )

  solicitud_tmp['conf']['items'] = items_envio
  solicitud = requests.request("POST", url, headers=headers, params=params, data=json.dumps(solicitud_tmp))
  if solicitud.status_code != 201:
    flash('Hubo un problema con la generación del evío. Error {}'.format(solicitud.status_code))
    loguear_error('crea_envio', 'Hubo un problema con la generación del evío', solicitud.status_code, json.dumps(solicitud) )
  else:
    almacena_envio(company, user, order, productos, solicitud.json())
  return solicitud.json()



def almacena_envio(company, user, order, productos, solicitud):
  if 'test' in session:  
    if session['test'] == 'True':
      url='../Boris_common/logs/pedido'+str(order.id)+'.json'
    else: 
      url="http://ec2-34-199-104-15.compute-1.amazonaws.com/pedidos"

  headers = {
    'Content-Type': 'application/json'
  }

  data = {
  "orden": order.id,
  "orden_nro": order.order_number,
  "orden_fecha": str(order.timestamp),
  "orden_medio_de_pago": order.metodo_de_pago,
  "orden_tarjeta_de_pago": order.tarjeta_de_pago,
  "correo":{
    "correo_id": solicitud['id'],
    "correo_status": solicitud['status'],
    "correo_precio": solicitud['price'],
    "correo_precio_formateado": solicitud['priceFormatted'],
    "correo_moneda":solicitud['currency'],
  },
  "cliente": {
    "id": user.id,
    "name": user.name,
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
      else: 
        flash('Se envio el pedido correctamente')

  



def cargar_pedido(unaEmpresa, pedido ):

  unCliente = Customer(
    id = pedido['customer']['id'],
    name =pedido['customer']['name'],
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
                        
  unaOrden = Order(
    id = pedido['id'],
    order_number = pedido['number'],
    order_original_id = pedido['id'],
    order_fecha_compra = datetime.strptime((pedido['completed_at']['date']), '%Y-%m-%d %H:%M:%S.%f'),
    metodo_de_pago = pedido['gateway'],
    tarjeta_de_pago = pedido['payment_details']['credit_card_company'],
    buyer = unCliente
    )       

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

  

def busca_tracking(orden):
  url = "http://ec2-34-199-104-15.compute-1.amazonaws.com/orden/tracking"
  params = {'orden_id': orden}
  historia = requests.request("GET", url, params=params).json()
  return historia


def loguear_error(modulo, mensaje, codigo, texto):
  outfile = open('app/logs/err_boris.txt', "a")
  outfile.write(str(datetime.utcnow())+','+ modulo +','+ mensaje +','+ str(codigo) +','+str(texto)+ '\n')
  outfile.close()


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
  

  
