import requests
import json
from app.models import Company
from flask import jsonify


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


def buscar_empresa():
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
  
 