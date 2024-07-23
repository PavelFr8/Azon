from flask import Blueprint

module = Blueprint('registration', __name__, url_prefix ='/login')

from app.modules.registration import routes