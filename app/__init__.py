import os

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_jwt_extended import JWTManager

from dotenv import load_dotenv

import logging


db = SQLAlchemy()  # create database
login_manager = LoginManager()  # create manager for login
csrf = CSRFProtect()  # create csrf protection
jwt = JWTManager()  # create jwt manager

# create logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def create_app():
    # create Flask app
    app = Flask(__name__)

    # get from .env app settings
    load_dotenv()
    settings = os.environ.get('APP_SETTINGS')
    app.config.from_object(settings)

    if app.debug == True:
        try:
            toolbar = DebugToolbarExtension(app)
        except Exception as e:
            app.logger.error(f"Failed to initialize DebugToolbarExtension: {e}")

    # register azon api
    import app.api.azon_api as azon_api
    app.register_blueprint(azon_api.module)

    # register azon REST api
    import app.api.restful_api as restful_api
    app.register_blueprint(restful_api.module)

    # register errors handler
    import app.errors as errors
    app.register_blueprint(errors.module)

    # register all app modules
    import app.modules.menu as menu
    app.register_blueprint(menu.module)

    import app.modules.registration as registration
    app.register_blueprint(registration.module)

    import app.modules.user_profile as user_profile
    app.register_blueprint(user_profile.module)

    import app.modules.shop as shop
    app.register_blueprint(shop.module)

    import app.modules.item as item
    app.register_blueprint(item.module)

    import app.modules.shopping_cart as shopping_cart
    app.register_blueprint(shopping_cart.module)

    import app.modules.location as location
    app.register_blueprint(location.module)

    import app.modules.paying as paying
    app.register_blueprint(paying.module)

    return app