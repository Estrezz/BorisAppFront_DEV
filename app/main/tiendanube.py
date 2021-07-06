import requests
import json
import datetime
from datetime import datetime
from app import db
from app.models import Customer, Order, Producto, Company, Store
from flask import session, flash, current_app, render_template



def buscar_pedido_tiendanube(empresa, form):
    url = "https://api.tiendanube.com/v1/"+str(empresa.store_id)+"/orders?q="+form.ordermail.data    
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
        ids_tmp = requests.request("GET", url, headers=headers, data=payload).json()
        for d in ids_tmp:
            ids.append(d['id'])
    return ids

##### prueba busqueda producto #####
def buscar_producto_tiendanube(empresa, desc_prod):
    url = "https://api.tiendanube.com/v1/"+str(empresa.store_id)+"/products?q="+desc_prod+"&fields=id,name"
    payload={}
    headers = {
        'Content-Type': 'application/json',
        'Authentication': empresa.platform_token_type+' '+empresa.platform_access_token
    }
    product = requests.request("GET", url, headers=headers, data=payload).json()
    #for i in product:
    #    flash('producto en Tiendanube {}- {}'.format(i, type(i)) )
    return product

def agregar_nota_tiendanube(company, order):
    url = "https://api.tiendanube.com/v1/"+str(company.store_id)+"/orders/"+str(order.order_original_id)
    data={
        "owner_note": "Esta orden tienen una gestión iniciada en BORIS",
    }
    headers = {
        'Content-Type': 'application/json',
        'Authentication': company.platform_token_type+' '+company.platform_access_token
    }
    requests.request("PUT", url, headers=headers, data=json.dumps(data))
    
