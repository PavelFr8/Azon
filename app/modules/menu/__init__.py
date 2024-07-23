from flask import Blueprint

module = Blueprint('menu', __name__, url_prefix ='/menu')

from app.modules.menu import routes