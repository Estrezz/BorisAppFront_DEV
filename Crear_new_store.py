
from app import  db, create_app
from app.models import Store

app=create_app()
with app.app_context():

  store = Store(
    platform = 'tiendanube',
    platform_access_token = 'ef879cb9fec5680cfb8f9dfd18b93f75542df4ba',
    platform_token_type = 'bearer',
    store_id = '630942',
    store_name = 'BATHINDA',
    store_url = ' https://www.bathinda.com.ar',
    store_country = 'AR',
    store_main_language = 'es',
    store_main_currency = 'ARS',
    admin_email = 'erezzoni@outlook.com',
    communication_email = 'soporte@borisreturns.com',
    param_logo = '//d2r9epyceweg5n.cloudfront.net/stores/630/942/themes/common/logo-1124427479-1610748605-3d629949685e1be6ea1bcaf0eab352571610748605.png?0',
    param_fondo = '',
    param_config = 'app/static/conf/bathinda.json',
    correo_usado = 'Ninguno',
    correo_apikey = '',
    correo_id = '',
    contact_name = '',
    contact_email = '',
    contact_phone = '+54 11 48135697',
    shipping_address = 'Uruguay',
    shipping_number = '1342',
    shipping_floor = '',
    shipping_zipcode = '',
    shipping_city = 'CABA',
    shipping_province = 'CABA',
    shipping_country = 'AR',
    shipping_info = ''
  )

  db.session.add(store)
  
  db.session.commit()

