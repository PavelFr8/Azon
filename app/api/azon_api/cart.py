from flask import flash, jsonify, abort
from flask_login import login_required, current_user

from app.api.azon_api import module
from app.models import ShoppingCart, Item
from app import db, logger


@module.route("/addToCart/<int:article>", methods=["POST"])
@login_required
def api_add_to_cart(article):
    try:
        item = Item.query.filter_by(article=article).first()
        shopping_cart: ShoppingCart = ShoppingCart.query.filter(ShoppingCart.user_id == current_user.id,
                                                                ShoppingCart.item_id == item.id).first()
        if shopping_cart:
            shopping_cart.amount += 1
        else:
            shopping_cart = ShoppingCart(
                user_id=current_user.id,
                item_id=item.id,
                amount=1
            )
        db.session.add(shopping_cart)
        db.session.commit()
        return jsonify({"success": True}), 201
    except Exception as e:
        logger.error(f"Error add item to shopping cart: {e}")
        db.session.rollback()
        flash("Произошла ошибка при сохранении в корзину", 'danger')
        return jsonify({"success": False}), 400