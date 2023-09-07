from flask import session, flash
from datetime import datetime


#################################################################################
# Valida ventana de cambios / devoluciones contra fecha de compra (o entrega)   #
# Valida que el rubro de los articulos no pertenezca a una categoria sin cambio #
#################################################################################
def validar_politica(fecha, prod_id):
  valida_rubro = validar_politica_rubro(prod_id)
  if valida_rubro[0] == 'Ninguno':
    return valida_rubro
  valida_fecha = validar_politica_fecha(fecha)
  return valida_fecha


#############################################
# Valida ventana de Cambio / Devolucion     #
#############################################
def validar_politica_fecha(orden_fecha):
    hoy = datetime.utcnow()
    periodo_cambio = session['ventana_cambio']
    periodo_devolucion = session['ventana_devolucion']

    dias_desde_orden = abs((hoy - orden_fecha).days)
    cambio = "OK" if dias_desde_orden <= periodo_cambio else "NOK"
    devolucion = "OK" if dias_desde_orden <= periodo_devolucion else "NOK"

    if cambio == "OK" and devolucion == "OK":
        resultado = ["Ambos", '']
    elif cambio == "OK" and devolucion == "NOK":
        resultado = ["Solo Cambio", ' El período para realizar devoluciones expiró ']
    elif cambio == "NOK" and devolucion == "OK":
        resultado = ["Solo Devolucion", ' El período para realizar cambios expiró ']
    else:
        resultado = ["Ninguno", ' El período para realizar cambios/devoluciones expiró ']

    #flash('Devolucion {} - periodo {} - {}'.format(devolucion, periodo_devolucion, abs((hoy - orden_fecha).days) ))
    return resultado


##################################################  
# Valida rubro vs categorias sin cambio          #
##################################################
def validar_politica_rubro(prod_id):
  if prod_id in session['ids_filtrados']:
    return ["Ninguno",'La categoria no acepta cambio / devolucion']
  else: 
    return ["rubro OK",'']