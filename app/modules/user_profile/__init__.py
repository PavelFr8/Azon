from flask import Blueprint

module = Blueprint('user_profile', __name__, url_prefix ='/user')

from app.modules.user_profile import routes