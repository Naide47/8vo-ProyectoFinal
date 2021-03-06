import os
from sqlalchemy import create_engine
import urllib


class Config(object):
    SECRET_KEY = 'Clave_Secret'
    SESSION_COOKIE_SECURE = False
    SECURITY_UNAUTHORIZED_VIEW = '/cerrarSesion'

class DevelopmentConfig(Config):
    DEBUG = True
    # Generamos la clave aleatoria de sesión Flask para crear una cookie con la inf. de la sesión
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SQLALCHEMY_DATABASE_URI = 'mysql://admin_c:cruz@localhost/imperioAlitasDB'
    