import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    DEBUG = False

    CSRF_ENABLED = True
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = os.environ.get("WTF_CSRF_SECRET_KEY")

    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_CSRF_CHECK_FORM = True

    SESSION_COOKIE_SECURE=True
    SESSION_COOKIE_HTTPONLY=True
    SESSION_COOKIE_SAMESITE="Lax"

    REMEMBER_COOKIE_SECURE=True
    REMEMBER_COOKIE_SAMESITE="Lax"

    SECRET_KEY = os.environ.get('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = os.environ.get('POSTGRESQL_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
