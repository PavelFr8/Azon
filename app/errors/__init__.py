from flask import Blueprint

module = Blueprint('errors', __name__)

from app.errors import handlers