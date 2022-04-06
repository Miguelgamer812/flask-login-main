class Config:
    SECRET_KEY = 'B!1w8NAt1T^%kvhUI*S^' #Llave para manejar agunos datos de inicio de sección como envio de mensajes atravez de la función flask


class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'flask-login'


config = {
    'development': DevelopmentConfig
}
    