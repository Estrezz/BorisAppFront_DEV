from datetime import datetime
from app import db


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    orders = db.relationship('Order', backref='buyer', lazy='dynamic')
    address = db.Column(db.String(64))
    number = db.Column(db.String(10))
    floor = db.Column(db.String(10))
    zipcode = db.Column(db.String(8))
    locality = db.Column(db.String(64))
    city = db.Column(db.String(64))
    Province = db.Column(db.String(64))
    country = db.Column(db.String(64))

    def __repr__(self):
        return '<Cliente {}>'.format(self.name)    

class Order(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.Integer)
    order_original_id = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    products = db.relationship('Producto', backref='articulos', lazy='dynamic')

    def __repr__(self):
        return '<Order {}>'.format(self.order_number)

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prod_id = db.Column(db.Integer, index=True)
    name = db.Column(db.String(120))
    price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    variant = db.Column(db.Integer)
    accion = db.Column(db.String(10))
    accion_reaccion = db.Column(db.Boolean)
    accion_cambiar_por = db.Column(db.Integer)
    accion_cantidad = db.Column(db.Integer)
    motivo = db.Column(db.String(50))
    image = db.Column(db.String(100))
    promo_descuento = db.Column(db.Float)
    promo_nombre = db.Column(db.String(10))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))

    def __repr__(self):
        return '<Product {}>'.format(self.name)

class Atributo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orden = db.Column(db.Integer) 
    descripcion = db.Column(db.String(20), index=True)

    def __repr__(self):
        return '<Atributo {}>'.format(self.descripcion)
