from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import LoginForm
from app.email import send_email
from app.models import Customer, Order, Producto
from app.interface import buscar_pedido
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
                unProducto = Producto(
                    id = pedido['products'][x]['id'],
                    name = pedido['products'][x]['name'],
                    price = pedido['products'][x]['price'],
                    quantity = pedido['products'][x]['quantity'],
                    #variant = pedido['products'][x]['variant'],
                    image = pedido['products'][x]['image']['src'],
                    accion = "Ninguna",
                    motivo =  "Ninguno",
                    articulos = unaOrden
                )
                db.session.add(unProducto)
                db.session.commit()

            #for i =1 to  in pedido['products']
            #   flash('ID {}'.format(i['id'])
            #    flash('NAME {}'.format(producto['name'])
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
    
    return render_template('pedido.html', title='Pedido', user=user, order = order, productos = productos)


@app.route('/envio_mail')
def envio_mail():
    send_email('prueba', 'erezzonico@borisreturns.com', 'erezzoni@outlook.com', 'esta es una prueba', '<h1>html_body</h1>')
    return render_template('envio.html', title='Envio de Mail')

