
from app import  db, create_app
from app.models import Company, Customer, Order, Producto

app=create_app()
with app.app_context():

  Producto.query.delete()  
  Order.query.delete()
  Customer.query.delete()
  Company.query.delete()


  db.session.commit()

