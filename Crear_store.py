
from app import db
from app.models import Store

Store.query.delete()

store1 = Store(
   platform = 'TiendaNube',
   store_id = '1447373',
   store_name = 'Demo Boris',
   admin_email = 'admin@borisreturns.com',
   param_logo = '/static/images/Demo_boris.png',
   param_fondo = '/static/images/logo1.png',
   param_config = 'app/static/conf/boris.json',
   correo_usado = 'Moova',
   correo_apikey = 'b23920003684e781d87e7e5b615335ad254bdebc',
   correo_id = 'b22bc380-439f-11eb-8002-a5572ae156e7',
   contact_name = 'Pepito Perez',
   contact_email = 'pepito@borisreturns.com',
   contact_phone = '+5491151064817',
   shipping_address = 'Virrey Loreto',
   shipping_number = '2259',
   shipping_floor = '',
   shipping_zipcode = '1426',
   shipping_city = 'CABA',
   shipping_province = 'CABA',
   shipping_country = 'AR',
   shipping_info = 'Entregar a pepito'
 )

db.session.add(store1)
db.session.commit()
