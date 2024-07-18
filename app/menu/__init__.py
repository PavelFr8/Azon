from flask import Blueprint

module = Blueprint('menu', __name__, url_prefix ='/')

from app.menu import routes