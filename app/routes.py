from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from app.email import send_email
from app.models import Customer, Orders
from app.interface import buscar_pedido
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
            flash('Order {}'.format(pedido))
            flash('Tipo {}'.format(type(pedido)))
            #flash('Order ID Tipo {}'.format(type(pedido['number'])))
            #flash('Producto {}'.format(pedido['products']))
                 
        return redirect(url_for('pedidos'))

    return render_template('buscar.html', title='Busca tu Pedido', form=form)


@app.route('/pedidos')
def pedidos():
    user = {'username': 'Usuario Prueba'}
    pedidos = [
        {
            'sku': 'A100B',
            'descripcion': 'Zapato DOS',
            'color': 'Azul',
            'cantidad': '1'
        },
        {
            'sku': 'A2009',
            'descripcion': 'Zapato UNO',
            'Color': 'Rojo',
            'cantidad': '2'
        }
    ]
    return render_template('pedidos.html', title='Pedidos', user=user, pedidos = pedidos)


@app.route('/envio_mail')
def envio_mail():
    send_email('prueba', 'erezzonico@borisreturns.com', 'erezzoni@outlook.com', 'esta es una prueba', '<h1>html_body</h1>')
    return render_template('envio.html', title='Envio de Mail')

