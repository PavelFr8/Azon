from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.exceptions import HTTPException

from app.api.api import module


def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    return payload, status_code


def bad_request(message):
    return error_response(400, message)


@module.errorhandler(HTTPException)
def handle_exception(e):
    return error_response(e.code)
