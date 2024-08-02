from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

import base64
import uuid

from app import db
from app.models import Shop, Item, Category
from . import api


# api resource for interaction with user shop
class ItemResource(Resource):
    @jwt_required()
    def get(self, article=None):
        if article:
            item = Item.query.filter_by(article=article).first_or_404()
            logo_url = f"/api/1.0/item/{article}/logo"
            categories = [Category.query.get(int(cat_id)).name for cat_id in item.category_id.split(',')]
            return make_response(jsonify({
                'name': item.name,
                'price': item.price,
                'about': item.about,
                'categories': categories,
                'logo_url': logo_url
            }), 200)
        else:
            return make_response(jsonify({'message': 'Missing item article'}), 400)

    @jwt_required()
    def post(self):
        data = request.get_json()
        name = data.get('name')
        price = data.get('price')
        about = data.get('about')
        shop_name = data.get('shop_name')
        shop = Shop.query.filter_by(name=shop_name, owner_id=get_jwt_identity()).first_or_404('Unknown shop')

        with open('app/static/img/header/logo.png', 'rb') as image_file:
            img_binary = base64.b64decode(base64.b64encode(image_file.read()))

        categories = [data.get('category1'), data.get('category2'), data.get('category3')]
        category_ids = []
        for category in categories:
            if category:
                ctgr = Category.query.filter_by(name=category).first()
                if ctgr:
                    category_ids.append(ctgr.id)
        if not category_ids:
            category_ids = [17, 17, 17]

        new_item = Item(
            name=name,
            article=int(str(int(uuid.uuid4()))[:13]),
            price=price,
            about=about,
            img=img_binary,
            category_id=','.join(map(str, category_ids)),
            seller_id=shop.id
        )
        db.session.add(new_item)
        db.session.commit()
        return make_response(jsonify({'message': 'Item successfully added'}), 201)

    @jwt_required()
    def put(self, article):
        data = request.get_json()
        item = Item.query.filter_by(article=article).first_or_404()

        if get_jwt_identity() != item.shop.owner_id:
            return make_response(jsonify({'message': 'Unauthorized'}), 403)

        if data.get('name'):
            item.name = data['name']
        if data.get('price'):
            item.price = data['price']
        if data.get('about'):
            item.about = data['about']

        categories = [data.get('category1'), data.get('category2'), data.get('category3')]
        category_ids = []
        for category in categories:
            if category:
                ctgr = Category.query.filter_by(name=category).first()
                if ctgr:
                    category_ids.append(ctgr.id)
        item.category_id = ','.join(map(str, category_ids))

        db.session.commit()
        return make_response(jsonify({'message': 'Item information successfully updated'}), 200)

    @jwt_required()
    def delete(self, article):
        item = Item.query.filter_by(article=article).first_or_404()
        if get_jwt_identity() != item.shop.owner_id:
            return jsonify({'message': 'Unauthorized'}), 403

        db.session.delete(item)
        db.session.commit()
        return make_response(jsonify({'message': 'Item successfully deleted'}), 204)


api.add_resource(ItemResource, '/shop/item', '/shop/item/<int:article>')
