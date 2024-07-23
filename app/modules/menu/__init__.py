from flask import Blueprint

module = Blueprint('menu', __name__)

from app.modules.menu import routes