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

