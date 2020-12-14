import requests
import json


url = "https://api.tiendanube.com/v1/1447373/orders?q=hotmail"   
## url = "https://api.tiendanube.com/v1/1447373/orders"
payload={}
headers = {
    'User-Agent': 'Boris (erezzonico@borisreturns.com)',
    'Content-Type': 'application/json',
    'Authentication': 'bearer cb9d4e17f8f0c7d3c0b0df4e30bcb2b036399e16'
    }
## order_tmp = requests.request("GET", url, headers=headers, data=payload).json()
## order_get = requests.get(url, headers=headers, data=payload)
## print(type(order_get))

## order = requests.request("GET", url, headers=headers, data=payload)
order = requests.request("GET", url, headers=headers, data=payload).json()

## print(order.headers['Date'])

## order_json = order.json()
print(type(order))

def buscar_nro_orden(lista, valor):
    for x in lista:
     if x['number'] == valor:
          print('found!!!')
          break
    else:
     print('No esta')

buscar_nro_orden(order,102)
##next((x for x in order if Order['number'] == 102), None)
print(order[0]['id']) ## Id de la compra
print(order[0]['number']) ## Nro de la compra

print(order[0]['customer']['email']) ## Mail del usuario qeu realizo la compra
print(order[0]['products']) ## Productos en la compra

print(len(order)) ## cantidad de Ordenes
print(len(order[0]['products'])) ## cantidad de productos


