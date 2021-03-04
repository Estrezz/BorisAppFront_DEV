
from app import  db, create_app
from app.models import Company, Customer, Order, Producto

app=create_app()
with app.app_context():

  Company.query.delete()
  Customer.query.delete()
  Order.query.delete()
  Producto.query.delete()

  db.session.commit()

