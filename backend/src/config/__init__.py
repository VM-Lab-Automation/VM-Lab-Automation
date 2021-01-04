import os


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE = 'vlab.db'
    JWT_SECRET = os.getenv('JWT_SECRET')


class ProductionConfig(Config):
    DATABASE = 'vlab.db'


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE = 'vlab.db'


class TestingConfig(Config):
    DEBUG = True
    DATABASE = 'test_db.db'
    JWT_SECRET = 'testing'
