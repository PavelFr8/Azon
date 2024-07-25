import os

from flask import Flask, flash
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from dotenv import load_dotenv

import logging


db = SQLAlchemy()  # create database
login_manager = LoginManager()  # create manager for login
logging.basicConfig(level=logging.DEBUG)
login_manager.session_protection = "strong"
logger = logging.getLogger(__name__)  # create logger


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

    return app