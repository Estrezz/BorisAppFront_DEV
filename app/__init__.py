from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_bootstrap import Bootstrap 
from flask_breadcrumbs import Breadcrumbs

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
bootstrap = Bootstrap(app)
Breadcrumbs(app=app)


app.config['MAIL_SERVER']='smtpout.secureserver.net'
app.config['MAIL_PORT'] = 3535
app.config['MAIL_USERNAME'] = 'erezzonico@borisreturns.com'
app.config['MAIL_PASSWORD'] = 'Dante1010!'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


from app import routes, models