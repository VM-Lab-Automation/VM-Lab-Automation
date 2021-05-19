import os


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_CONNECTION_STRING = ''
    JWT_SECRET = os.getenv('JWT_SECRET')


class ProductionConfig(Config):
    DATABASE_CONNECTION_STRING = os.getenv('DATABASE_CONNECTION_STRING')


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_CONNECTION_STRING = os.getenv('DATABASE_CONNECTION_STRING')


class TestingConfig(Config):
    DEBUG = True
    DATABASE_CONNECTION_STRING = ''
    JWT_SECRET = 'testing'
