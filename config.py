import os
from sqlalchemy import create_engine
import urllib

class Config(object):
    SECRET_KEY='Clave_Secret'
    SECRET_COOKIE_SECRET=False
    
class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI='mysql://admin_c:cruz@localhost/pizzas'
    
    
    