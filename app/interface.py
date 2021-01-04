import requests
import json
from app import db
from app.models import Customer, Order, Producto, Company, Store
from flask import jsonify, flash


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
  promo = ("",0)
  for x in promociones: 
    if x['id'] == Id_Producto:
      promo = (x['discount_script_type'], x['discount_amount'])
      return promo
  return promo
  

#############################################################################
# Busca alternativas para cambiar un articulo según el motivo de cambio
# devuelve lista con productos alternativos
#############################################################################
def buscar_alternativas(storeid, prod_id, motivo, item_variant):
  url = "https://api.tiendanube.com/v1/"+str(storeid)+"/products/"+str(prod_id)+"/variants"
  
  payload={}
  headers = {
    'User-Agent': 'Boris (erezzonico@borisreturns.com)',
    'Content-Type': 'application/json',
    'Authentication': 'bearer cb9d4e17f8f0c7d3c0b0df4e30bcb2b036399e16'
   }
  variantes_tmp = requests.request("GET", url, headers=headers, data=payload).json()
  variantes = []

  for x in variantes_tmp:
    if x['stock'] > 1 and x['id'] != item_variant :
      variantes.append(x)

  return variantes


def buscar_empresa(empresa):
  if empresa != 'Ninguna':
    empresa_tmp = Store.query.filter(Store.store_id == empresa).first()
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
    unaEmpresa = Company(
      platform = 'TiendaNube',
      store_id = '1447373',
      company_name = 'Tienda Boris',
      admin_email = 'admin@borisreturns.com',
      logo = '/images/logo1.png',
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

  



def crea_envio(company, user, order, productos):

  url = "https://api-dev.moova.io/b2b/shippings"

  headers = {
    'Authorization': 'API_KEY',
    'application_id': 'b22bc380-439f-11eb-8002-a5572ae156e7',
    'Content-Type': 'application/json',
    'API_KEY': 'b23920003684e781d87e7e5b615335ad254bdebc'
   }

  solicitud = {
        "currency" :'ARS',
        "type" : 'regular',
        "flow" : 'semi-automatc',
        "from" : {
            "street": user.address,
            "number": user.number,
            "floor": user.floor,
            "apartment": "",
            "city": user.city,
            "state": user.province,
            "postalCode": user.zipcode,
            "country": user.country,
            "instructions": "",
            "contact": {
                "firstName": user.name,
                "lastName": "",
                "email": user.email,
                "phone": user.phone
            }
        }
    }

  #solicitud_correo = requests.request("POST", url, headers=headers, data=jsonify(solicitud))
  #flash('interface {}'.format(solicitud_correo))
  return solicitud


def cargar_pedido(unaEmpresa, pedido ):

  #unaEmpresa = buscar_empresa(storeid)

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
      accion_cantidad = pedido['products'][x]['quantity'],
      promo_descuento = promo_tmp[1],
      promo_nombre = promo_tmp[0],
      articulos = unaOrden
      )
  db.session.add(unProducto)
  db.session.commit()