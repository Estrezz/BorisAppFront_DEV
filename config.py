import os
import redis
from dotenv import load_dotenv



basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))



class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super secret key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['soporte@borisreturns.com']
    SERVER_ROLE = os.environ.get('SERVER_ROLE')

    SESSION_TYPE = os.environ.get('SESSION_TYPE')
    SESSION_REDIS = redis.from_url(os.environ.get('SESSION_REDIS'))
    

    