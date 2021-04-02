
from app import  db, create_app
from app.models import Store

app=create_app()
with app.app_context():



  Store.query.delete()

  store1 = Store(
    platform = 'tiendanube',
    platform_access_token = 'd3209f9f749a749ee205e2f0e150f732bbe8b997',
    platform_token_type = 'bearer',
    store_id = '1631829',
    store_name = 'demo debocaenboca',
    store_country = 'AR',
    store_main_language = 'es',
    store_main_currency = 'ARS',
    admin_email = 'leilasaid@hotmail.com',
    communication_email = 'soporte@borisreturns.com',
    param_logo = '//d2r9epyceweg5n.cloudfront.net/stores/001/631/829/themes/common/logo-343539575-1617381511-501e7beeaea7770b915d4300c320ad871617381511.png?0',
    param_fondo = '/static/images/logo1.png',
    param_config = 'app/static/conf/Leila.json',
    correo_usado = 'Ninguno',
    correo_apikey = '',
    correo_id = '',
    contact_name = 'Leila Almacen',
    contact_email = 'erezzoni@yahoo.com',
    contact_phone = '4500 4500',
    shipping_address = 'Virrey Loreto',
    shipping_number = '2253',
    shipping_floor = '',
    shipping_zipcode = '1426',
    shipping_city = 'CABA',
    shipping_province = 'CABA',
    shipping_country = 'AR',
    shipping_info = 'dejar en recepcion'
  )

  db.session.add(store1)

  store2 = Store(
    platform = 'tiendanube',
    platform_access_token = 'cb9d4e17f8f0c7d3c0b0df4e30bcb2b036399e16',
    platform_token_type = 'bearer',
    store_id = '1447373',
    store_name = 'Demo Boris',
    store_country = 'AR',
    store_main_language = 'es',
    store_main_currency = 'ARS',
    admin_email = 'erezzoni@yahoo.com',
    communication_email = 'soporte@borisreturns.com',
    param_logo = '/static/images/Demo_boris.png',
    param_fondo = '/static/images/logo1.png',
    param_config = 'app/static/conf/boris.json',
    correo_usado = 'Moova',
    correo_apikey = 'b23920003684e781d87e7e5b615335ad254bdebc',
    correo_id = 'b22bc380-439f-11eb-8002-a5572ae156e7',
    correo_test = True,
    correo_apikey_test = 'b23920003684e781d87e7e5b615335ad254bdebc',
    correo_id_test = 'b22bc380-439f-11eb-8002-a5572ae156e7',
    contact_name = 'Boris Almacen',
    contact_email = 'erezzoni@yahoo.com',
    contact_phone = '4800 4800',
    shipping_address = 'Virrey Loreto',
    shipping_number = '2259',
    shipping_floor = '',
    shipping_zipcode = '1426',
    shipping_city = 'CABA',
    shipping_province = 'CABA',
    shipping_country = 'AR',
    shipping_info = 'dejarselo a Pepito'
  )
  db.session.add(store2)
  
  db.session.commit()

