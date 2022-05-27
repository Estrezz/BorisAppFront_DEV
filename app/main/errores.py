import datetime
from datetime import datetime
from flask import session, current_app, flash


############################## loguea_error ##################################################
def loguear_error_general(modulo, mensaje, codigo, texto):
    url = "logs/app/errores_generales_log.txt"
    outfile = open(url, "a+")
    outfile.write(str(datetime.utcnow())+','+ modulo +','+ mensaje +','+ str(codigo) +','+str(texto)+ '\n')
    outfile.close()
