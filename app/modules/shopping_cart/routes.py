from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user

import base64

from app.models import Item, User, ShoppingCart
from app import db, logger
from . import module


# Добавление товара в корзину
@module.route('/add/<int:id>')
@login_required
def add(id):
    try:
        shopping_cart: ShoppingCart = ShoppingCart.query.filter(ShoppingCart.user_id == current_user.id,
                                                                ShoppingCart.item_id == id).first()
        if shopping_cart:
            shopping_cart.amount += 1
        else:
            shopping_cart = ShoppingCart(
                user_id=current_user.id,
                item_id=id,
                amount=1
            )
        db.session.add(shopping_cart)
        db.session.commit()
        return redirect(url_for("item.profile", id=id))
    except Exception as e:
        logger.error(f"Error add item to shopping cart: {e}")
        db.session.rollback()
        flash("Произошла ошибка при сохранении в корзину", 'danger')


# Отображение корзины
@module.route('/')
@login_required
def cart():
    total_price = 0
    items = []
    shopping_carts = ShoppingCart.query.filter_by(user_id=current_user.id).all()
    for cart in shopping_carts:
        item: Item = Item.query.get(cart.item_id)
        total_price += item.price
        item.logo_data = base64.b64encode(item.img).decode('utf-8') if item.img else None
        item.amount = cart.amount
        items.append(item)
    return render_template('shopping_cart/cart.html', title='Корзина', items=items, total_price=total_price)


# Удаление товара из корзины
@module.route('/delete/<int:id>')
@login_required
def delete(id):
    try:
        shopping_cart: ShoppingCart = ShoppingCart.query.filter(ShoppingCart.user_id == current_user.id,
                                                                ShoppingCart.item_id == id).first()
        db.session.delete(shopping_cart)
        db.session.commit()
        return redirect(url_for('shopping_cart.cart'))
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error delete item from shopping cart: {e}")
        flash("Произошла ошибка при удалении товара из корзины", 'danger')
