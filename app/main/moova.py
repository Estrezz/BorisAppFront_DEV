import requests
import json
from flask import session, flash


def crea_envio_moova(company, user, order, productos): 
    if 'shipping' in session:  
        if session['shipping'] == 'customer':
            paga_correo = 'manual'
        else: 
            # paga_correo ='semi-automatic'
            # Comentado hasta comprobar que funcion al 100%
            # al activar hay que agregar etiqueta en el mail
            paga_correo ='manual'
    else:
        paga_correo ='manual'

    #crea archivo para el envio
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
        "instructions": user.instructions,
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

    ### Usa ambiente de desarrollo de MOOVA
    if session['correo_test'] == 'True':
        url = "https://api-dev.moova.io/b2b/shippings"
        headers = {
        'Authorization': company.correo_apikey,
        'Content-Type': 'application/json',
        }
        params = {'appId': company.correo_id}

    ### Usa ambiente de PRODUCCION de MOOVA
    if session['correo_test'] == 'False':
        url = "https://api-prod.moova.io/b2b/shippings"
        headers = {
        'Authorization': company.correo_apikey,
        'Content-Type': 'application/json',
        }
        params = {'appId': company.correo_id}
  
    solicitud = requests.request("POST", url, headers=headers, params=params, data=json.dumps(solicitud_tmp))
    if solicitud.status_code != 201:
        flash('Hubo un problema con la generación del evío. Error {}'.format(solicitud.status_code))
        #loguear_error('crea_envio', 'Hubo un problema con la generación del evío', solicitud.status_code, solicitud.json() )
        return 'Failed'
    else:
        return solicitud.json()
    

#### Cotiza Costo del envio con la empresa MOOVA
def cotiza_envio_moova(company, user, order, productos):
    solicitud_tmp = {
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
    "conf": {
        "assurance": False,
        "items": [
        ]
    },
    "shipping_type_id": 1
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

    ### Usa ambiente de desarrollo de MOOVA
    if session['correo_test'] == 'True':
        url = "https://api-dev.moova.io//b2b/v2/budgets"
        headers = {
        'Authorization': company.correo_apikey,
        'Content-Type': 'application/json',
        }
        params = {'appId': company.correo_id}

    ### Usa ambiente de PRODUCCION de MOOVA
    if session['correo_test'] == 'False':
        url = "https://api-prod.moova.io/b2b/v2/budgets"
        headers = {
        'Authorization': company.correo_apikey,
        'Content-Type': 'application/json',
        }
        params = {'appId': company.correo_id}

    solicitud_tmp = requests.request("POST", url, headers=headers, params=params, data=json.dumps(solicitud_tmp))
    if solicitud_tmp.status_code != 200:
        #flash('Hubo un problema con la generación del evío. Error {}'.format(solicitud_tmp.status_code))
        #flash('Hubo un problema con la generación del evío. Error {} '.format(solicitud_tmp.json()))
        return 'Failed'
    else:
        solicitud = solicitud_tmp.json()
        #flash('El precio del envio es {}'.format(solicitud_tmp.price_formatted))
        precio = solicitud['price_formatted']
        return precio

