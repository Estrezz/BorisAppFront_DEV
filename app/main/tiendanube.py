import requests
import json
from datetime import datetime, timedelta
from app import db
from flask import session, flash, current_app
from app.main.errores import loguear_error_general
from app.models import Customer, Order, Producto
from app.main.funciones import validar_politica



def buscar_pedido_tiendanube(empresa, ordermail, ordernum):

    url = f"https://api.tiendanube.com/v1/{empresa.store_id}/orders?q={ordermail}&fields=id,number&per_page=100"
    payload={}
    headers = {
        'Content-Type': 'application/json',
        'Authentication': f"{empresa.platform_token_type} {empresa.platform_access_token}"
    }

    try:
        response = requests.request("GET", url, headers=headers, data=json.dumps(payload))

        #print(response.status_code, response.reason)
        
        if response.status_code == 504:
                return "TIMEOUT"

        # If NOT FOUND trata de resolver el problema del 5xx
        if response.status_code == 404 or response.status_code == 500:
                #print('----------500-----------------')
                reason = response.reason
                description = response.json().get("description")

                if (description and "Obtained" in description) or response.status_code == 500:
                # if "Obtained" in response.json().get("description", ""):
                    # Calculate today's date and 30 days ago
                    today = datetime.now().date()
                    thirty_days_ago = today - timedelta(days=45)
                    
                    # Format the dates as strings
                    today_str = today.isoformat()
                    thirty_days_ago_str = thirty_days_ago.isoformat()
                    
                    # Update the URL with the new created_at_min parameter
                    url = f"https://api.tiendanube.com/v1/{empresa.store_id}/orders?q={ordermail}&fields=id,number&per_page=50&created_at_min={thirty_days_ago_str}"
                    print (url)
                    response = requests.request("GET", url, headers=headers, data=json.dumps(payload))
                    #print('response2--------------')
                    #print(response.status_code)
                    if response.status_code != 200:
                        return"REINTENTAR"
                else :
                    return "NOTFOUND"

        # Si el response es exitoso, filtra las ordenes y busca la orden por ID
        if response.status_code == 200:
            order_list = response.json()

            if not order_list:
                return "NOTFOUND"

            for x in order_list:
                if x['number'] == ordernum:
                    order_url = f"https://api.tiendanube.com/v1/{empresa.store_id}/orders/{x['id']}"
                    order_response = requests.get(order_url, headers=headers, data=json.dumps(payload))
                    order = order_response.json()
                    return order
      
    except requests.exceptions.RequestException as e:
        return 'None'
    except json.JSONDecodeError as e:
        return 'None'


############################## carga_pedido ##################################################
def cargar_pedido_tiendanube(unaEmpresa, pedido ):

  # CHeck error
#   if isinstance(pedido, dict):
#         # Check if 'customer' is a dictionary within pedido
#         if 'customer' in pedido and isinstance(pedido['customer'], dict):
#             # Check if 'id' is present in the 'customer' dictionary
#            if 'id' not in pedido['customer']:
#                 loguear_error_general('Error en Pedido-Customer-ID', "'id' not present in 'customer' dictionary.", unaEmpresa.store_id, pedido )
#         else:
#             loguear_error_general('Error en Pedido-Customer-ID', "'customer' is not a dictionary within pedido.", unaEmpresa.store_id, pedido )
#   else:
#         loguear_error_general('Error en Pedido-Customer-ID', " pedido is not a dictionary", unaEmpresa.store_id, pedido )
#     ### End of check error  

  unCliente = Customer(
      customer_uid = str(session['uid']),
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
  session['cliente'] = unCliente.customer_uid


  #### Si el pedido ya tiene una nota la carga #########################
  if pedido['owner_note'] and pedido['owner_note'] != "Esta orden tienen una gestión iniciada en BORIS":
    nota = pedido['owner_note'] + " - Esta orden tienen una gestión iniciada en BORIS"
  else:
    nota = "Esta orden tienen una gestión iniciada en BORIS"

  
  unaOrden = Order(
      order_uid = str(session['uid']),
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
      owner_note = nota,
      buyer = unCliente
      )
  session['orden'] = unaOrden.order_uid      

  for producto in pedido['products']:
    promo_tmp = buscar_promo_tiendanube(pedido['promotional_discount']['contents'], producto['id'])
    valida = validar_politica(unaOrden.order_fecha_compra, producto['product_id'] )
    precio_tmp = producto['price'] if producto['price'] else 0

    unProducto = Producto(
        id =  producto['id'],
        prod_id = producto['product_id'],
        name = producto['name'],
        price = precio_tmp,
        quantity = producto['quantity'],
        alto = producto['height'],
        largo = producto['width'],
        profundidad = producto['depth'],
        peso = producto['weight'],
        variant = producto['variant_id'],
        image = producto['image']['src'],
        accion = "ninguna",
        motivo =  "",
        politica_valida = valida[0],
        politica_valida_motivo = valida[1],
        accion_cantidad = producto['quantity'],
        promo_precio_final = promo_tmp[2],
        promo_descuento = promo_tmp[1],
        promo_nombre = promo_tmp[0],
        articulos = unaOrden
      )

    db.session.add(unProducto)
  db.session.commit()
  return("Pedido Tiendanube Cargado")


def buscar_pedido_conNro_tiendanube(empresa, orderid):
    url = "https://api.tiendanube.com/v1/"+str(empresa.store_id)+"/orders/"+orderid
    payload={}
    headers = {
        'Content-Type': 'application/json',
        'Authentication': empresa.platform_token_type+' '+empresa.platform_access_token
    }
    order = requests.request("GET", url, headers=headers, data=payload).json()
    return order


################## Devuelve las alternativas configuradas en la tienda para el articulo  ##################
def buscar_alternativas_tiendanube(empresa, storeid, prod_id, item_variant):
    url = f"https://api.tiendanube.com/v1/{storeid}/products/{prod_id}"
    headers = {
        'Content-Type': 'application/json',
        'Authentication': empresa.platform_token_type+' '+empresa.platform_access_token
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 404:
        return response.status_code
    
    product = response.json()

    #### Si no se gestiona el stock o el Id de la variante es igual
    #### en la descripcion cambia el texto a "Mismo Articulo" 
    variantes = []
    for x in product['variants']:    
        if (x['stock'] is None or x['stock'] > 0) and x['id'] == item_variant:
            x['values'] = [{"es": "Mismo Articulo"}]
        
        if x['stock'] is not None and x['stock'] <= 0:
            continue
        
        element = {"id": x['id'], "values":x['values']}
        
        variantes.append(element)
    
    atributos = []
    for atributo in product['attributes']:
        atributos.append(atributo['es'])

    return variantes, atributos
    

############################ Devuelve el nombre del producto en español ###########################
def buscar_producto_nombre_tiendanube(empresa, storeid, prod_id):
    url = f"https://api.tiendanube.com/v1/{storeid}/products/{prod_id}?fields=name"
    #payload={}
    headers = {
        'Content-Type': 'application/json',
        'Authentication': empresa.platform_token_type+' '+empresa.platform_access_token
    }

    response = requests.get(url, headers=headers)
   
    if response.status_code == 404:
        return response.status_code
    
    product = response.json()
    return product['name']['es']


def validar_categorias_tiendanube(company):
    ids =[]
    for i in session['rubros']:
        url = "https://api.tiendanube.com/v1/"+str(company.store_id) +"/products?category_id="+str(i)+"&fields=id"
        payload={}
        headers = {
        'Content-Type': 'application/json',
        'Authentication': company.platform_token_type+' '+company.platform_access_token
        }
        ids_tmp = requests.request("GET", url, headers=headers, data=payload)
        if ids_tmp.status_code == 200:
            ids_tmp = ids_tmp.json()
            for d in ids_tmp:
                ids.append(d['id']) 
        else:
            loguear_error_general('Error en CATEGORIAS', 'No existe la categoria', company.store_id, url )
               
        # else registrar que categoris es la que no existe   
    return ids


def buscar_producto_tiendanube(empresa, desc_prod):
    ### ocultos
    url = "https://api.tiendanube.com/v1/"+str(empresa.store_id)+"/products?q="+desc_prod+"&fields=id,name,published"
    payload={}
    headers = {
        'Content-Type': 'application/json',
        'Authentication': empresa.platform_token_type+' '+empresa.platform_access_token
    }
    
    productos_tmp = requests.request("GET", url, headers=headers, data=payload).json()
    ## filtra los productos ocultos
    if 'code' in productos_tmp:
       productos = {}
    else: 
        productos = [{"id":p['id'],"name":p['name']['es']} for p in productos_tmp if p['published'] == True]

    print(productos)     
    return productos


def agregar_nota_tiendanube(company, order):
    url = "https://api.tiendanube.com/v1/"+str(company.store_id)+"/orders/"+str(order.order_original_id)

    #https://api.tiendanube.com/v1/1698970/orders/438624469?fields=id,owner_note
    
    headers = {
        'Content-Type': 'application/json',
        'Authentication': company.platform_token_type+' '+company.platform_access_token
    }
    payload={}
    
    data={
        "owner_note": order.owner_note,
    }
    requests.request("PUT", url, headers=headers, data=json.dumps(data))


#############################################################################
# Busca la promo con la que se vendió un articulo 
# devuelve [nombre promo. precio promocional]
#############################################################################
def buscar_promo_tiendanube(promociones, Id_Producto ):
  promo = ("",0,0)
  for x in promociones:
    if x['id'] == Id_Producto:
      ### correccion PROMO -- si la orden tiene error el tipo de x['discount_script_type'] es DICT####
      if isinstance(x['discount_script_type'], str):
        promo = (x['discount_script_type'], x['discount_amount'], x['final_price'])
      # return promo
  return promo

  
