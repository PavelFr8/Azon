from flask import Blueprint

module = Blueprint('paying', __name__, url_prefix ='/pay')

from app.modules.paying import routes