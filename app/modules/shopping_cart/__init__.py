from flask import Blueprint

module = Blueprint('shopping_cart', __name__, url_prefix ='/shopping_cart')

from app.modules.shopping_cart import routes