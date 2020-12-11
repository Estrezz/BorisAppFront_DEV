from datetime import datetime
from app import db



class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    phone = db.Column(db.String(20))
    identification = db.Column(db.String(20), index=True)
    default_address = db.Column(db.String(120))
    addresses = db.Column(db.String(120))
    total_spent = db.Column(db.Integer)
    active = db.Column(db.Boolean)
    last_order_id = db.Column(db.Integer)
    orders = db.relationship('Orders', backref='Customer', lazy='dynamic')

    def __repr__(self):
        return '<Cliente {}>'.format(self.name)    


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer,index=True)
    customer = db.Column(db.String(120), index=True)
    products = db.Column(db.String(120),index=True)
    coupon = db.Column(db.String(120))
    discount = db.Column(db.Integer)
    subtotal = db.Column(db.Integer)
    total = db.Column(db.Integer)
    currency = db.Column(db.String(120))
    language = db.Column(db.String(120))
    shipping = db.Column(db.String(120))
    shipping_cost_owner = db.Column(db.Integer)
    shipping_cost_customer = db.Column(db.Integer)
    shipping_pickup_details = db.Column(db.String(120))
    storefront = db.Column(db.String(120))
    shipping_status = db.Column(db.String(120))
    payment_status = db.Column(db.String(120))
    next_Action = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, index=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))

    def __repr__(self):
        return '<Order {}>'.format(self.number)

  