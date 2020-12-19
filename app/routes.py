from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import LoginForm
from app.email import send_email
from app.models import Customer, Order, Producto
from app.interface import buscar_pedido, buscar_promo, buscar_alternativas
from flask import request
import requests


@app.route('/', methods=['GET', 'POST'])

@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    form = LoginForm()
    if form.validate_on_submit():
        pedido = buscar_pedido(1447373, form)

        if pedido == 'None':
            flash('No se encontro un pedido para esa combinación Pedido-Email')
            return render_template('buscar.html', title='Busca tu Pedido', form=form)
        else:
            ## Borrar todos los datos de la base de datos ##
            Customer.query.delete()
            Order.query.delete()
            Producto.query.delete()
            db.session.commit()
            #### fin borrado #################################

            unCliente = Customer(
                id = pedido['customer']['id'],
                name =pedido['customer']['name'],
                email = pedido['customer']['email']
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
                    #variant = pedido['products'][x]['variant'],
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
            
            #flash('Order {}'.format(pedido))
            #flash('Tipo {}'.format(type(pedido)))
            #flash('Order ID Tipo {}'.format(type(pedido['number'])))
            #flash('Cliente {}'.format(pedido['customer']))
            #flash('Producto {}'.format(pedido['products']))
            #flash('Producto {}'.format(pedido['products'][0]['image']['src']))
            #flash('Producto Cantidad {}'.format(len(pedido['products']))) 
            #flash('Producto {}'.format(pedido['products'][0]))   
            #flash('Producto {}'.format(pedido['products'][0]['id']))            
            #flash('Producto tipo {}'.format(type(pedido['products'])))
            return redirect(url_for('pedidos'))

    return render_template('buscar.html', title='Busca tu Pedido', form=form)


@app.route('/pedidos', methods=['GET', 'POST'])
def pedidos():
    user = Customer.query.first()
    order = Order.query.first()
    productos = Producto.query.all()

    if request.method == "POST" and request.form.get("form_item") == "elegir_item" : 
        prod_id = request.form.get("Prod_Id")
        accion = request.form.get(str("accion"+request.form.get("Prod_Id")))
        accion_cantidad = request.form.get(str("accion_cantidad"+request.form.get("Prod_Id")))
        motivo = request.form.get(str("motivo"+request.form.get("Prod_Id")))
        item = Producto.query.get(prod_id)
        item.accion = accion
        item.accion_reaccion = False 
        item.accion_cantidad = accion_cantidad
        item.motivo = motivo
        db.session.commit()

        if accion == 'cambiar' and item.accion_reaccion == False:
            alternativas = buscar_alternativas(1447373, item.prod_id, motivo)
            user = Customer.query.first()
            order = Order.query.first()
            item = Producto.query.get(prod_id)
            return render_template('devolucion.html', title='Cambio', user=user, order = order, item = item, alternativas = alternativas)

    if request.method == "POST" and request.form.get("form_item") == "cambiar_item" :
        opciones = request.form.to_dict(flat=True)
        for i in request.form :
            flash('Item i {}'.format(type(i)))
            flash('Item i {}'.format(request.form.get(i)))
    
    return render_template('pedido.html', title='Pedido', user=user, order = order, productos = productos)


@app.route('/pedidos_unitarios', methods=['GET', 'POST'])
def pedidos_unitarios():   

    if request.method == "POST": 
        prod_id = request.form.get("Prod_Id")
        user = Customer.query.first()
        order = Order.query.first()
        item = Producto.query.get(prod_id)
    
    return render_template('devolucion.html', title='Accion', user=user, order = order, item = item)

@app.route('/Confirmar',methods=['GET', 'POST'])
def confirma_cambios():
    user = Customer.query.first()
    order = Order.query.first()
    # productos = Producto.query.all()
    productos = Producto.query.filter((Producto.accion != 'ninguna'))

    return render_template('pedido_confirmar.html', title='Confirmar', user=user, order = order, productos = productos)

@app.route('/envio_mail')
def envio_mail():
    send_email('prueba', 'erezzonico@borisreturns.com', 'erezzoni@outlook.com', 'esta es una prueba', '<h1>html_body</h1>')
    return render_template('envio.html', title='Envio de Mail')


@app.route('/buscar_aletrnativa2',methods=['GET', 'POST'])
#############################################################################
# Busca alternativas para cambiar un articulo según el motivo de cambio
# devuelve lista con productos alternativos
#############################################################################
def buscar_aletrnativa2(storeid, prod_id, motivo):
  url = "https://api.tiendanube.com/v1/"+str(storeid)+"/products/"+str(prod_id)+"/variants"
    
  payload={}
  headers = {
    'User-Agent': 'Boris (erezzonico@borisreturns.com)',
    'Content-Type': 'application/json',
    'Authentication': 'bearer cb9d4e17f8f0c7d3c0b0df4e30bcb2b036399e16'
   }
  variantes = requests.request("GET", url, headers=headers, data=payload).json()
  
  return variantes



