from flask import flash, jsonify
from flask_login import login_required, current_user

from app.api.azon_api import module
from app.models import ShoppingCart, Item
from app import db, logger



# Delete item from shop
@module.route("/deleteFromShop/<int:article>", methods=["DELETE"])
@login_required
def delete_item(article):
    item = Item.query.filter_by(article=article).first_or_404()
    if not current_user.id == item.shop.owner_id:
        raise Exception
    try:
        # Удаляем товар из корзины каждого пользователя, у которого он есть
        carts_with_item = ShoppingCart.query.filter_by(item_id=item.id).all()
        for cart in carts_with_item:
            db.session.delete(cart)

        db.session.delete(item)
        db.session.commit()
        return jsonify({"success": True}), 204
    except Exception as e:
        db.session.rollback()
        logger.error(f"Ошибка при удалении товара: {e}")
        flash("Произошла ошибка при удалении товара.", 'danger')
        return jsonify({"success": False}), 400