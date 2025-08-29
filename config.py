from datetime import timedelta


class Config:
    #FLASK_ENV='development'
    #ENV='development'
    DEBUG = 1
    FLASK_DEBUG = 1
    HOST = '0.0.0.0'
    PORT = 50001
    SQLALCHEMY_DATABASE_URI = 'sqlite:///teste.db?check_same_thread=False'
    MASTER_KEY = '123456'