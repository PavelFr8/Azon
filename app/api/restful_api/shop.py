from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

import base64

from app import db
from app.models import Shop, Item
from . import api


# api resource for interaction with items in the shop
class ShopResource(Resource):
    @jwt_required()
    def get(self, shop_name=None):
        if shop_name:
            shop = Shop.query.filter_by(name=shop_name).first_or_404()
            items = Item.query.filter_by(seller_id=shop.id).all()
            logo_url = f"/api/1.0/shop/{shop_name}/logo"

            items_data = [{
                'name': item.name,
                'price': item.price,
                'about': item.about,
                'logo_url': f"/api/1.0/item/{item.article}/logo"
            } for item in items]

            return make_response(jsonify({
                'shop': {
                    'name': shop.name,
                    'about': shop.about,
                    'contact': shop.contact,
                    'logo_url': logo_url
                },
                'items': items_data
            }), 200)
        else:
            return make_response(jsonify({'message': 'Missing shop_name'}), 400)

    @jwt_required()
    def post(self):
        data = request.get_json()
        name = data['name']
        if Shop.query.filter_by(name=name).first():
            return make_response(jsonify({'message': 'Shop with this name already exists'}), 400)

        with open('app/static/img/header/logo.png', 'rb') as image_file:
            img_binary = base64.b64decode(base64.b64encode(image_file.read()))

        new_shop = Shop(
            name=name,
            about=data.get('about'),
            img=img_binary,
            owner_id=get_jwt_identity(),
            contact=data.get('contact')
        )
        db.session.add(new_shop)
        db.session.commit()
        return make_response(jsonify({'message': 'Shop successfully registered'}), 201)

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

        db.session.commit()
        return make_response(jsonify({'message': 'Shop information successfully updated'}), 200)

    @jwt_required()
    def delete(self, shop_name=None):
        if shop_name:
            shop = Shop.query.filter_by(name=shop_name, owner_id=get_jwt_identity()).first_or_404()
            db.session.delete(shop)
            db.session.commit()
            return make_response(jsonify({'message': 'Successfully delete shop'}), 204)
        else:
            return make_response(jsonify({'message': 'Missing shop_name'}), 400)


api.add_resource(ShopResource, '/shop', '/shop/<string:shop_name>')