from flask import request, jsonify, make_response
from flask_jwt_extended import create_access_token

from app.models import User
from . import module


# User sing in and get his JWT access token
@module.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return make_response(jsonify({'message': 'Invalid email or password'}), 401)

    access_token = create_access_token(identity=user.id)
    return make_response(jsonify({'access_token': access_token}), 200)