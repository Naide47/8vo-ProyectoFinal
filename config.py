import os
import urllib

from sqlalchemy import create_engine


class Config(object):
    SECRET_KEY = 'Clave_Secret'
    SESSION_COOKIE_SECURE = False


class DevelopmentConfig(Config):
    DEBUG = True
    #Generamos la clave aleatoria de sesión Flask para crear una cookie con la inf. de la sesión
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    #Definimos la ruta a la BD: mysql://user:password@localhost/bd'
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:root@localhost/imperioAlitasBD'
