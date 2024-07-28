from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user

import base64

from app.models import ShoppingCart, Item
from app import db, logger
from . import module


# Добавление товара в корзину
@module.route('/add/<int:article>', methods=['POST'])
@login_required
def add(article):
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
    except Exception as e:
        logger.error(f"Error add item to shopping cart: {e}")
        db.session.rollback()
        flash("Произошла ошибка при сохранении в корзину", 'danger')


# Отображение корзины
@module.route('/')
@login_required
def cart():
    total_price = 0
    items = current_user.get_items_in_cart()
    for item in items:
        total_price += item.price
    return render_template('shopping_cart/cart.html', title='Корзина', items=items, total_price=total_price)


# Удаление товара из корзины
@module.route('/delete/<int:article>')
@login_required
def delete(article):
    try:
        item = Item.query.filter_by(article=article).first()
        shopping_cart: ShoppingCart = ShoppingCart.query.filter(ShoppingCart.user_id == current_user.id,
                                                                ShoppingCart.item_id == item.id).first()
        db.session.delete(shopping_cart)
        db.session.commit()
        return redirect(url_for('shopping_cart.cart'))
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error delete item from shopping cart: {e}")
        flash("Произошла ошибка при удалении товара из корзины", 'danger')
