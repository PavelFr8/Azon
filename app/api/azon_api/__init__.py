from flask import Blueprint
from flask_cors import CORS

module = Blueprint('api', __name__, url_prefix='/api')
CORS(module, origins=['https://azon-azjx.onrender.com', 'https://example.com'])

from app.api.azon_api import errors, cart, item