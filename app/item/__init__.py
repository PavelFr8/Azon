from flask import Blueprint

module = Blueprint('item', __name__, url_prefix ='/item')

from app.item import routes