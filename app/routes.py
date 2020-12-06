from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')    


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}'.format(form.ordernum.data))
        return redirect('/pedidos')

    return render_template('login.html', title='Busca tu Pedido', form=form)


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

