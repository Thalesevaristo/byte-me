import os
from re import DEBUG


class Config(object):
    TESTING = False
    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = "dev"
    SQLALCHEMY_DATABASE_URI = "sqlite:///byteme.sqlite"
    JWT_SECRET_KEY = "$cadush@DEV"


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SECRET_KEY = "test"
    DATABASE_URI = "sqlite:///:memory:"
    JWT_SECRET_KEY = "$cadush@TEST"
