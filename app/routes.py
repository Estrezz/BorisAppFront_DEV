from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from app.email import send_email
from app.models import Customer, Orders
import requests

@app.route('/', methods=['GET', 'POST'])
@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    form = LoginForm()
    if form.validate_on_submit():

        flash('Buscar pedido Nro {}'.format(form.ordernum.data))
        
        url = "https://api.tiendanube.com/v1/1447373/orders?q"+form.ordermail.data
        payload={}
        headers = {
            'User-Agent': 'Boris (erezzonico@borisreturns.com)',
            'Content-Type': 'application/json',
            'Authentication': 'bearer cb9d4e17f8f0c7d3c0b0df4e30bcb2b036399e16'
        }
        order = requests.request("GET", url, headers=headers, data=payload).json()
        flash('Mail {}'.format(form.ordermail))
        flash('URL {}' .format(url))
        flash('Order {}'.format(order))

        ## commit orden / ordenes ##

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

