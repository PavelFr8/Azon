from flask import Blueprint
from flask_restful import Api

from app import csrf

module = Blueprint('api', __name__, url_prefix='/api/1.0')

# create api
api = Api(module)

csrf.exempt(module)

from app.api.restful_api import shop, errors, images, login, items
