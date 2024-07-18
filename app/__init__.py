import os

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])

    if app.debug == True:
        try:
            toolbar = DebugToolbarExtension(app)
        except Exception as e:
            app.logger.error(f"Failed to initialize DebugToolbarExtension: {e}")

    import app.menu as menu
    app.register_blueprint(menu.module)

    import app.registration as registration
    app.register_blueprint(registration.module)

    return app

from . import models