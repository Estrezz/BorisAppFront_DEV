import requests
import json
import datetime
from datetime import datetime
from app import db
from flask import session, flash, current_app
from app.main.errores import loguear_error_general
from app.models import Customer, Order, Producto
from app.main.funciones import validar_politica



########################################################################
# Busca la orden en Shopify usando el Mail y nro de orden provistos    #
########################################################################
def buscar_pedido_shopify(empresa, ordernum, ordermail):
    url = f"{empresa.company_url}/admin/api/2023-04/orders.json?email={ordermail}"
   
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': empresa.platform_access_token
    }
    response = requests.request("GET", url, headers=headers).json()

    for order in response['orders']:
        if str(order['order_number']) == ordernum:
            return order

    return 'None'


#########################################################
#### Carga en memoria la orden                          #
#########################################################
def cargar_pedido_shopify(unaEmpresa, pedido ):

    unCliente = Customer(
      customer_uid = str(session['uid']),
      id = pedido['customer']['id'],
      name =pedido['customer']['first_name']+" "+pedido['customer']['last_name'],
      ##### REVISAR - ver donde se encuentra el documento del cliente
      # identification = pedido['customer']['identification'],
      ###############
      email = pedido['customer']['email'],
      phone = pedido['customer']['phone'],
      address = pedido['shipping_address']['address1'],
      zipcode = pedido['shipping_address']['zip'],
      city = pedido['shipping_address']['city'],
      province = pedido['shipping_address']['province'],
      country = pedido['shipping_address']['country'],
      ##### REVISAR - No vienen en la direccion de la orden de Shopify
      number = "",
      floor = "",
      locality = "",
      pertenece = unaEmpresa
      )
    session['cliente'] = unCliente.customer_uid
    
    #### Si el pedido ya tiene una nota la carga #########################
    nota_actual = pedido['note'] if pedido['note'] != None else ""
    nota = f"{nota_actual} - " if nota_actual != "Esta orden tienen una gestión iniciada en BORIS" else ""
    nota += "Esta orden tienen una gestión iniciada en BORIS"

    datetime_str = pedido['processed_at']
    datetime_str = datetime_str[:-3] + datetime_str[-2:]
    datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S%z')
    
    
    unaOrden = Order(
      order_uid = str(session['uid']),
      id = pedido['id'],
      order_number = pedido['order_number'],
      order_original_id = pedido['id'],
      order_fecha_compra = datetime_obj.replace(tzinfo=None),
      ### REVISAR - payment_gateways_name es un array y puede ser mas de uno
      metodo_de_pago = ['payment_gateway_names'][0],
      ### REVISAR - ver de donde sacar datos de la tarjeta
      #tarjeta_de_pago = pedido['payment_details']['credit_card_company'],
      ### REVISAR - para gastos_cupon se puso el total Ver si hay variaciones y guardar currency en el presentment currency 
      gastos_cupon = pedido['total_discounts'],
      #gastos_gateway = pedido['discount_gateway'],
      gastos_shipping_owner = pedido['total_shipping_price_set']['presentment_money']['amount'],
      #gastos_shipping_customer = pedido['shipping_cost_customer'],
      # gastos_promocion = pedido['promotional_discount']['total_discount_amount'],
      owner_note = nota,
      buyer = unCliente
      )
    session['orden'] = unaOrden.order_uid      

    for producto in pedido['line_items']:
        #promo_tmp = buscar_promo_shopify(pedido['promotional_discount']['contents'], pedido['products'][x]['id'] )
        valida = validar_politica(unaOrden.order_fecha_compra, producto['product_id'] )

        ### Busca imagen del producto
        url = f"{unaEmpresa.company_url}/admin/api/2023-04/products/{producto['product_id']}.json"
        headers = {
            'Content-Type': 'application/json',
            'X-Shopify-Access-Token': unaEmpresa.platform_access_token
        }
        product_atributes = requests.request("GET", url, headers=headers).json()
        
        precio_tmp = producto['price'] if producto['price'] else 0
        
        if producto['discount_allocations'] and len(producto['discount_allocations']) > 0:
            precio_promo_tmp = producto['discount_allocations'][0]['amount'] 
            precio_promo_final_tmp = str(float(precio_tmp) - float(precio_promo_tmp))
            promo_name_tmp = pedido['discount_applications'][producto['discount_allocations'][0]['discount_application_index']]['title']

        else:   
            precio_promo_tmp = 0
            precio_promo_final_tmp = 0
            promo_name_tmp = ""


        # Busca datos de la variante
        #for item in product_atributes['product']['variants']:
        #    if item['id'] == producto['variant_id']:
        #        variante = item
        
        unProducto = Producto(
            id =  producto['id'],
            prod_id = producto['product_id'],
            name = producto['name'],
            price = float(precio_tmp),
            quantity = producto['quantity'],
            #### REVISAR - ver de donde sacar alto, largo y profundidad
            alto = 0,
            largo = 0,
            profundidad = 0,
            #### FIN REVISAR ############################3##########
            peso = producto['grams'],
            variant = producto['variant_id'],
            ## Guaradar Variant Title
            image = product_atributes['product']['images'][0]['src'],
            accion = "ninguna",
            motivo =  "",
            politica_valida = valida[0],
            politica_valida_motivo = valida[1],
            accion_cantidad = producto['quantity'],
            promo_precio_final = precio_promo_final_tmp,
            promo_descuento = precio_promo_tmp,
            promo_nombre = promo_name_tmp,
            articulos = unaOrden
        )

        db.session.add(unProducto)
    db.session.commit()
    return ("Pedido Shopify Cargado")


def buscar_alternativas_shopify(empresa, storeid, prod_id, item_variant):
    url = f"{empresa.company_url}/admin/api/2023-04/products/{prod_id}.json"
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': empresa.platform_access_token
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 404:
        return response.status_code
    
    product = response.json()
    
    #### copiado de tiendanube
    variantes = []
    for x in product['product']['variants']:
        if (x['inventory_quantity'] is None or x['inventory_quantity'] > 0) and x['id'] == item_variant:
            x['values'] = [{"es": "Mismo Articulo"}]
        if x['inventory_quantity'] > 0:
            x['values'] = [{"es": x['title']}]
            #variantes.append(x)
        element = {"id": x['id'], "values":x['values']}
        
        variantes.append(element)
    
    atributos = []
    for atributo in product['product']['options']:
        atributos.append(atributo['name'])

    return variantes, atributos


def buscar_producto_shopify(empresa, desc_prod):
    #### Como buscar todos los que tienen una descripcion
    url = f"{empresa.company_url}/admin/api/2023-04/graphql.json"
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': empresa.platform_access_token
    }
    
    query = "{\"query\":\"{\\r\
                products(first: 100, query:\\\"title:"+str({desc_prod})+"*\\\") {\\r\
                    edges {\\r\
                        node {\\r\
                            id\\r\
                            title\\r\
                            productType\\r\
                            status\\r\
                        }\\r\
                    }\\r\
                }\\r\
            }\\r\
            \\r\
            \",\"variables\":{}}"
            
    response = requests.request("POST", url, headers=headers, data=query)
    if response.status_code == 404:
        productos = {}
    
    productos_tmp = response.json()
    
    productos = [{"id": p['node']['id'].split("gid://shopify/Product/")[1], "name":p['node']['title']} for p in productos_tmp['data']['products']['edges'] if p['node']['status'] == 'ACTIVE']
    
    return productos

############################ Devuelve el nombre del producto en español ###########################
def buscar_producto_nombre_shopify(empresa, storeid, prod_id):
    url = f"{empresa.company_url}/admin/api/2023-04/products/{prod_id}.json?fields=title"
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': empresa.platform_access_token
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 404:
        productos = {}
    
    productos = response.json()
    
    return productos['product']['title']
