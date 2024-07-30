from flask import Blueprint

module = Blueprint('location', __name__, url_prefix ='/address')

from app.modules.location import routes