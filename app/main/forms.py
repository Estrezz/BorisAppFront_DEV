from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    ordernum = IntegerField('Número de Orden', validators=[DataRequired()])
    ordermail = StringField('Email con el que se realizó la compra', validators=[DataRequired()])
    submit = SubmitField('Buscar')

class DireccionForm(FlaskForm):
    name = StringField('Nombre y Apellido', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    phone = StringField('Telefono') 
    address = StringField('Calle', validators=[DataRequired()]) 
    number = StringField('Numero', validators=[DataRequired()])
    floor = StringField('Piso')
    zipcode = StringField('Codigo Postal', validators=[DataRequired()])
    locality = StringField('Localidad', validators=[DataRequired()])
    city = StringField('Ciudad', validators=[DataRequired()])
    province = StringField('Provincia', validators=[DataRequired()])
    country = StringField('Pais', validators=[DataRequired()])
    submit = SubmitField('Guardar')