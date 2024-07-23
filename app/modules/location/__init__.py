from flask import Blueprint

module = Blueprint('location', __name__, url_prefix ='/location')

from app.modules.location import routes