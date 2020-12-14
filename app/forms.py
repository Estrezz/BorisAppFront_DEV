from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    ordernum = IntegerField('Orden', validators=[DataRequired()])
    ordermail = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Buscar')
