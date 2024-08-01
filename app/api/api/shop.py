from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

import base64

from app import db
from app.models import Shop, Item, User
from app.utils.allowed_file import allowed_file
from . import module, api


# Вход пользователя и выдача JWT токена
@module.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    user: User = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid email or password'}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token}), 200


class ShopResource(Resource):
    @jwt_required()
    def get(self, shop_name=None):
        if shop_name:
            shop = Shop.query.filter_by(name=shop_name).first_or_404()
            items = Item.query.filter_by(seller_id=shop.id).all()
            logo_data = base64.b64encode(shop.img).decode('utf-8') if shop.img else None

            items_data = [{
                'name': item.name,
                'price': item.price,
                'logo_data': base64.b64encode(item.img).decode('utf-8') if item.img else None
            } for item in items]

            return jsonify({
                'shop': {
                    'name': shop.name,
                    'about': shop.about,
                    'contact': shop.contact,
                    'logo_data': logo_data
                },
                'items': items_data
            })
        else:
            # Получить список всех магазинов
            shops = Shop.query.all()
            return jsonify([{'name': shop.name, 'contact': shop.contact} for shop in shops])

    @jwt_required()
    def post(self):
        data = request.get_json()
        if Shop.query.filter_by(name=data['name']).first():
            return jsonify({'message': 'Shop with this name already exists'}), 400

        img_file = request.files.get('img')
        if allowed_file(img_file.filename):
            img_binary = img_file.read() if img_file else None
        else:
            return jsonify({'message': 'Wrong img format'})

        new_shop = Shop(
            name=data['name'],
            about=data.get('about'),
            img=img_binary,
            owner_id=get_jwt_identity(),
            contact=data['contact']
        )
        db.session.add(new_shop)
        db.session.commit()
        return jsonify({'message': 'Shop successfully registered'}), 201

    @jwt_required()
    def put(self, shop_name):
        data = request.get_json()
        shop = Shop.query.filter_by(name=shop_name, owner_id=get_jwt_identity()).first_or_404()

        if data.get('name'):
            shop.name = data['name']
        if data.get('about'):
            shop.about = data['about']
        if data.get('contact'):
            shop.contact = data['contact']

        img_file = request.files.get('img')
        if img_file:
            shop.img = img_file.read()

        db.session.commit()
        return jsonify({'message': 'Shop information successfully updated'})

    @jwt_required()
    def delete(self, item_id=None):
        if item_id:
            item = Item.query.filter_by(id=item_id).first_or_404()
            if get_jwt_identity() != item.shop.seller_id:
                return jsonify({'message': 'Unauthorized'}), 403

            db.session.delete(item)
            db.session.commit()
            return jsonify({'message': 'Item successfully deleted'}), 204
        else:
            return jsonify({'message': 'Missing shop_name or item_id'}), 400


api.add_resource(ShopResource, '/shop', '/shop/<string:shop_name>', '/shop/item/<int:item_id>')
