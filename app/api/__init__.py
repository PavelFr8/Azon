from flask import Blueprint

module = Blueprint('api', __name__, url_prefix='/api')

from app.api import errors