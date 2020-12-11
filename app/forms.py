from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    ordernum = StringField('Orden', validators=[DataRequired()])
    ordermail = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Buscar')
