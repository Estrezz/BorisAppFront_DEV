from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import LoginForm, DireccionForm
from app.email import send_email
from app.models import Customer, Order, Producto, Company
from app.interface import buscar_pedido, buscar_promo, buscar_alternativas, buscar_empresa, crea_envio, cargar_pedido, buscar_pedido_conNro
from flask import request
import requests


@app.route('/', methods=['GET', 'POST'])

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.args.get('store_id') == None:
        return redirect(url_for('buscar', empresa = 'Ninguna'))    
    else:
        if request.args.get('order_id') == None:
            return redirect(url_for('buscar', empresa = request.args.get('store_id')))
        else: 
            unaEmpresa = buscar_empresa(request.args.get('store_id'))
            pedido = buscar_pedido_conNro(unaEmpresa.store_id, request.args.get('order_id'))
            cargar_pedido(unaEmpresa, pedido)
            return redirect(url_for('pedidos'))


@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    ## Borrar todos los datos de la base de datos ##
    Company.query.delete()
    Customer.query.delete()
    Order.query.delete()
    Producto.query.delete()
    db.session.commit()
    #### fin borrado #################################

    unaEmpresa = buscar_empresa(request.args['empresa'])

    form = LoginForm()
    if form.validate_on_submit():
        pedido = buscar_pedido(unaEmpresa.store_id, form)

        if pedido == 'None':
            flash('No se encontro un pedido para esa combinación Pedido-Email')
            return render_template('buscar.html', title='Inicia tu gestión', form=form, store=unaEmpresa.company_name, logo=unaEmpresa.logo)
        else:
            cargar_pedido(unaEmpresa, pedido)
            return redirect(url_for('pedidos'))

    return render_template('buscar.html', title='Inicia tu Gestión', form=form, store=unaEmpresa.company_name, logo=unaEmpresa.logo)


@app.route('/pedidos', methods=['GET', 'POST'])
def pedidos():
    company = Company.query.first()
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
            item = Producto.query.get(prod_id)
            alternativas = buscar_alternativas(1447373, item.prod_id, motivo, item.variant)
            user = Customer.query.first()
            order = Order.query.first()
            item = Producto.query.get(prod_id)
            return render_template('devolucion.html', title='Cambio', user=user, order=order, item=item, alternativas=alternativas)

    if request.method == "POST" and request.form.get("form_item") == "cambiar_item" :
        prod_id = request.form.get("Prod_Id")
        item = Producto.query.get(prod_id)
        item.accion_reaccion = True
        item.accion_cambiar_por = request.form.get("variante")
        db.session.commit() 

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


@app.route('/direccion', methods=['GET', 'POST'])
def direccion():
    user = Customer.query.first()
    form = DireccionForm()
    if request.method == 'GET':
        form.address.data = user.address
        form.number.data = user.number
        form.floor.data = user.floor
        form.zipcode.data = user.zipcode
        form.locality.data = user.locality
        form.city.data = user.city
        form.province.data = user.province
        form.country.data = user.country
    if form.validate_on_submit():
        form.populate_obj(obj=user)
        db.session.commit() 
        return redirect(url_for('confirma_cambios'))
    return render_template('direccion.html', form=form, user=user)


@app.route('/confirma_solicitud', methods=['GET', 'POST'])
def confirma_solicitud():
    company = Company.query.first()
    user = Customer.query.first()
    order = Order.query.first()
    productos = Producto.query.filter((Producto.accion != 'ninguna'))
    crea_envio(company, user, order, productos)
    return render_template('envio.html', company = company, user = user, order = order, productos = productos)



@app.route('/envio_mail')
def envio_mail():
    send_email('prueba', 'erezzonico@borisreturns.com', 'erezzoni@outlook.com', 'esta es una prueba', '<h1>html_body</h1>')
    return render_template('envio.html', title='Envio de Mail')


  



