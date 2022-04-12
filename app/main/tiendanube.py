import requests
import json
from app import db
from flask import session, flash, current_app
from app.main.errores import loguear_error_general



def buscar_pedido_tiendanube(empresa, ordermail):
    url = "https://api.tiendanube.com/v1/"+str(empresa.store_id)+"/orders?q="+ordermail    
    payload={}
    headers = {
        'Content-Type': 'application/json',
        'Authentication': empresa.platform_token_type+' '+empresa.platform_access_token
    }
    order_tmp = requests.request("GET", url, headers=headers, data=payload).json()
    return order_tmp



def buscar_pedido_conNro_tiendanube(empresa, orderid):
    url = "https://api.tiendanube.com/v1/"+str(empresa.store_id)+"/orders/"+orderid
    payload={}
    headers = {
        'Content-Type': 'application/json',
        'Authentication': empresa.platform_token_type+' '+empresa.platform_access_token
    }
    order = requests.request("GET", url, headers=headers, data=payload).json()
    return order


def buscar_alternativas_tiendanube(empresa, storeid, prod_id):
    url = "https://api.tiendanube.com/v1/"+str(storeid)+"/products/"+str(prod_id)
    payload={}
    headers = {
        'Content-Type': 'application/json',
        'Authentication': empresa.platform_token_type+' '+empresa.platform_access_token
    }
    product = requests.request("GET", url, headers=headers, data=payload).json()
    ### Si no exsite el producto -- Se da cuando el Merchant elimina el producto adquirido ###
    if 'code' in product.keys():
        if product['code'] == 404:
            return product['code']
    #####
    return product


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
    url = "https://api.tiendanube.com/v1/"+str(empresa.store_id)+"/products?q="+desc_prod+"&fields=id,name"
    payload={}
    headers = {
        'Content-Type': 'application/json',
        'Authentication': empresa.platform_token_type+' '+empresa.platform_access_token
    }
    product = requests.request("GET", url, headers=headers, data=payload).json()
    return product


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
