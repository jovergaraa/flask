from decouple import config

#Configuracion para que tome el .env y poder conectar a la base de datos
class Config():
    SECRET_KEY = config('SECRET_KEY')

class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'development': DevelopmentConfig
}