from flask import render_template
from werkzeug.exceptions import HTTPException

from app import db, logger
from . import module

@module.app_errorhandler(404)
def not_found_error(error):
    logger.error(f"404 error: {error}")
    return render_template('errors/404.html'), 404

@module.app_errorhandler(500)
def internal_error(error):
    logger.error(f"500 error: {error}")
    db.session.rollback()
    return render_template('errors/500.html'), 500

@module.app_errorhandler(400)
def bad_request_error(error):
    logger.error(f"400 error: {error}")
    return render_template('errors/400.html'), 400

@module.app_errorhandler(403)
def forbidden_error(error):
    logger.error(f"403 error: {error}")
    return render_template('errors/403.html'), 403

@module.app_errorhandler(405)
def method_not_allowed_error(error):
    logger.error(f"405 error: {error}")
    return render_template('errors/405.html'), 405

@module.app_errorhandler(401)
def method_not_allowed_error(error):
    return render_template('errors/401.html'), 401

@module.app_errorhandler(Exception)
def handle_unexpected_error(error):
    logger.error(f"Unexpected error: {error}")
    if isinstance(error, HTTPException):
        return render_template(f"errors/{error.code}.html"), error.code
    return render_template('errors/500.html'), 500
