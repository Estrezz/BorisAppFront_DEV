import requests
import json

from app import app


def buscar_nro_pedido(lista, valor):
    for x in lista:
     if x['number'] == valor:
          return x
    else:
     return 'None'


def buscar_pedido(storeid, form):
  url = "https://api.tiendanube.com/v1/"+str(storeid)+"/orders?q="+form.ordermail.data    
  ## url = "https://api.tiendanube.com/v1/1447373/orders?q"+form.ordermail.data
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
def buscar_alternativas(storeid, prod_id, motivo):
  #url = "https://api.tiendanube.com/v1/"+str(storeid)+"/products/"+str(prod_id)+"/variants"
  url = "https://api.tiendanube.com/v1/"+str(storeid)+"/products/"+str(prod_id)
  
  payload={}
  headers = {
    'User-Agent': 'Boris (erezzonico@borisreturns.com)',
    'Content-Type': 'application/json',
    'Authentication': 'bearer cb9d4e17f8f0c7d3c0b0df4e30bcb2b036399e16'
   }
  producto = requests.request("GET", url, headers=headers, data=payload).json()
  
  # carga los atributos del producto para ver en que posicion estan Talle y Color
  # para buscar despues las alternativas que correspondan segun el motivo
  atributos = []
  for i in range(len(producto['attributes'])):
    atributos.append([producto['attributes'][i]['es'],i])
  
  ######################################################
  ## Calcula las variantes existentes 
  ## arma diccionario {atributo : [valores]}
  ######################################################
  opciones = {}
  for i in range(len(producto['attributes'])):
    _key = producto['attributes'][i]['es']
    for x in producto['variants']:
      _val = x['values'][i]['es']
      if _key in opciones:
        opciones[_key].append(_val)
      else:
        opciones[_key] = [_val]
  
  #### extrae los valor duplicados """"
  for k in opciones:
    opciones_set = set(opciones[k])
    opciones[k] = list(opciones_set)

  return opciones
