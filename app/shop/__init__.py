from flask import Blueprint

module = Blueprint('shop', __name__, url_prefix ='/shop')

from app.shop import routes