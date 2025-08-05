class Config:
    SECRET_KEY = 'AVERYSECRETKEY123415515'
    DEBUG = False
    PORT = 3040
    HOST = '0.0.0.0'

class DevelopmentConfig(Config):
    DEBUG = True
    PORT = 3040

class ProductionConfig(Config):
    DEBUG = False
    PORT = 3040
