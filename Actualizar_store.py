
from app import  db, create_app
from app.models import Store

app=create_app()
with app.app_context():

  store = Store.query.filter_by(store_id='138327').first()
  
  db.session.delete(store)

  #store.store_name = 'Abundancia por designio'
  #store.param_logo = 'https://frontprod.borisreturns.com/static/images/abundancia.png'

  #store = Store(
  #  platform = 'tiendanube',
  #  platform_access_token = '89a5ea6c862b1955d4e42f111f2685a0584c5de7',
  #  platform_token_type = 'bearer',
  #  store_id = '138327',
  #  store_name = 'abundanciapordesignio',
  #  store_url = '  https://www.abundancia.com.ar',
  #  store_country = 'AR',
  #  store_main_language = 'es',
  #  store_main_currency = 'ARS',
  #  admin_email = 'lucia@abundanciapordesignio.com',
  # communication_email = 'soporte@borisreturns.com',
  #  param_logo = '//d2r9epyceweg5n.cloudfront.net/stores/138/327/themes/common/logo-712739697-1617662790-c06459b7d6059be019bb87615059f7bf1617662790.jpg?0',
  #  param_fondo = '',
  #  param_config = 'app/static/conf/abundancia.json',
  #  correo_usado = 'Ninguno',
  #  correo_apikey = '',
  #  correo_id = '',
  #  contact_name = '',
  #  contact_email = 'info@abundanciapordesignio.com',
  #  contact_phone = '',
  #  shipping_address = 'Showroon Balvanera ',
  #  shipping_number = '',
  #  shipping_floor = '',
  #  shipping_zipcode = '',
  #  shipping_city = 'CABA',
  #  shipping_province = 'CABA',
  #  shipping_country = 'AR',
  #  shipping_info = ''
  #)

  # db.session.add(store)
  
  db.session.commit()

