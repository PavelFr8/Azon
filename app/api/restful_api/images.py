from flask import jsonify, send_file
from flask_restful import Resource

from io import BytesIO

from app.models import Shop, Item
from . import api


# api resource for interaction with items and shops logos
class ImageResource(Resource):
    def get(self, shop_name=None, article=None):
        if shop_name:
            shop = Shop.query.filter_by(name=shop_name).first_or_404()
            if shop.img:
                img_binary = shop.img
                return send_file(BytesIO(img_binary), mimetype='image/jpeg')
            else:
                return jsonify({'message': 'Image not found'}), 404
        elif article:
            item = Item.query.filter_by(article=article).first_or_404()
            if item.img:
                img_binary = item.img
                return send_file(BytesIO(img_binary), mimetype='image/jpeg')
            else:
                return jsonify({'message': 'Image not found'}), 404


api.add_resource(ImageResource, '/shop/<string:shop_name>/logo', '/item/<int:article>/logo')
