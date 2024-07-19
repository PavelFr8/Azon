import os

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from dotenv import load_dotenv


db = SQLAlchemy()  # create database
login_manager = LoginManager()  # create manager for login


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

    # register all app modules
    import app.menu as menu
    app.register_blueprint(menu.module)

    import app.registration as registration
    app.register_blueprint(registration.module)

    import app.user_profile as user_profile
    app.register_blueprint(user_profile.module)

    return app

from . import models