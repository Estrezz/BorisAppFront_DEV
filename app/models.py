from datetime import datetime
from app import db

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(64))
    platform_token_type = db.Column(db.String(30))
    platform_access_token = db.Column(db.String(64))
    store_id = db.Column(db.String(64), index=True)
    company_main_language = db.Column(db.String(20))
    company_main_currency = db.Column(db.String(20))
    company_country = db.Column(db.String(20))
    company_name = db.Column(db.String(64))
    company_url = db.Column(db.String(120))
    admin_email = db.Column(db.String(120))
    communication_email = db.Column(db.String(120))
    communication_email_name = db.Column(db.String(120))
    logo = db.Column(db.String(200))
    fondo = db.Column(db.String(200))
    param_config = db.Column(db.String(120))
    contact_name = db.Column(db.String(64))
    contact_phone = db.Column(db.String(20))
    contact_email = db.Column(db.String(120))
    correo_usado = db.Column(db.String(64))
    correo_apikey = db.Column(db.String(50))
    correo_id = db.Column(db.String(50))
    correo_test = db.Column(db.Boolean)
    correo_apikey_test = db.Column(db.String(50))
    correo_id_test = db.Column(db.String(50))
    shipping_address = db.Column(db.String(64))
    shipping_number = db.Column(db.String(64))
    shipping_floor = db.Column(db.String(64))
    shipping_zipcode = db.Column(db.String(64))
    shipping_city = db.Column(db.String(64))
    shipping_province = db.Column(db.String(64))
    shipping_country = db.Column(db.String(64))
    shipping_info = db.Column(db.String(120))
    company_uid = db.Column(db.String(150))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    clientes = db.relationship('Customer', backref='pertenece', lazy='dynamic')

class Customer(db.Model):
    customer_uid = db.Column(db.String(150), primary_key=True)
    id = db.Column(db.Integer, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete='CASCADE'))
    name = db.Column(db.String(64), index=True)
    identification = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True)
    phone = db.Column(db.String(20))
    orders = db.relationship('Order', backref='buyer', lazy='dynamic')
    address = db.Column(db.String(180))
    number = db.Column(db.String(35))
    floor = db.Column(db.String(100))
    zipcode = db.Column(db.String(8))
    locality = db.Column(db.String(250))
    city = db.Column(db.String(64))
    province = db.Column(db.String(64))
    country = db.Column(db.String(64))
    instructions = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Cliente {}>'.format(self.name)    

class Order(db.Model):
    order_uid = db.Column(db.String(150), primary_key=True)
    id =  db.Column(db.Integer, nullable=False)
    order_number = db.Column(db.Integer)
    order_original_id = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    order_fecha_compra = db.Column(db.DateTime)
    metodo_de_pago = db.Column(db.String(35))
    tarjeta_de_pago = db.Column(db.String(25))
    gastos_cupon = db.Column(db.Float)
    gastos_gateway = db.Column(db.Float)
    gastos_shipping_owner = db.Column(db.Float)
    gastos_shipping_customer = db.Column(db.Float)
    gastos_promocion = db.Column(db.Float)
    owner_note = db.Column(db.String(500))
    salientes = db.Column(db.String(10)) # Indica si la orden tiene articulos salientes
    customer_id = db.Column(db.String(150), db.ForeignKey('customer.customer_uid', ondelete='CASCADE'))
    products = db.relationship('Producto', backref='articulos', lazy='dynamic')

    def __repr__(self):
        return '<Order {}>'.format(self.order_number)

class Producto(db.Model):
    #order_id = db.Column(db.Integer, db.ForeignKey('order.order_uid', ondelete='CASCADE'), primary_key=True)
    order_id = db.Column(db.String(150), db.ForeignKey('order.order_uid', ondelete='CASCADE'), primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    prod_id = db.Column(db.Integer, index=True)
    name = db.Column(db.String(120))
    price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    variant = db.Column(db.Integer)
    alto = db.Column(db.Float)
    largo = db.Column(db.Float)
    profundidad = db.Column(db.Float)
    peso = db.Column(db.Float)
    accion = db.Column(db.String(10))
    accion_reaccion = db.Column(db.Boolean)
    accion_cambiar_por = db.Column(db.Integer)
    accion_cambiar_por_prod_id = db.Column(db.Integer)
    accion_cambiar_por_desc = db.Column(db.String(100))
    accion_cantidad = db.Column(db.Integer)
    motivo = db.Column(db.String(150))
    politica_valida = db.Column(db.String(50))
    politica_valida_motivo = db.Column(db.String(100))
    image = db.Column(db.String(300))
    promo_descuento = db.Column(db.Float)
    promo_nombre = db.Column(db.String(10))
    promo_precio_final = db.Column(db.Float)
    observaciones = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Product {}>'.format(self.name)

class Atributo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orden = db.Column(db.Integer) 
    descripcion = db.Column(db.String(20), index=True)

    def __repr__(self):
        return '<Atributo {}>'.format(self.descripcion)

