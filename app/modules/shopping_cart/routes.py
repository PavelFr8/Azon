from flask import request, render_template, abort, redirect, url_for
from flask_login import login_required

import base64

from app.models import Item, Shop, Category, User
from app import db
from app.utils.allowed_file import allowed_file
from . import module


# Добавление товара в корзину
@app.route('/add_to_cart/<int:id>')
@login_required
def add_to_cart(id):
    db_sess = get_db_session()
    item: Item = db_sess.query(Item).get(id)
    user: User = db_sess.query(User).get(current_user.id)
    if item and user:
        if user.shopping_cart:
            cart = user.shopping_cart.split(',')
            if f'{item.id}' not in cart:
                user.shopping_cart += f',{item.id}'
        else:
            user.shopping_cart = item.id
        db_sess.commit()
    return redirect(url_for('item_profile', id=id))


# Отображение корзины
@app.route('/cart')
@login_required
def cart():
    db_sess = get_db_session()
    items_in_cart = []
    items = []
    total_price = 0
    if current_user.shopping_cart:
        items_in_cart = [int(id) for id in current_user.shopping_cart.split(',') if id]
    if items_in_cart:
        items = db_sess.query(Item).filter(Item.id.in_(items_in_cart)).all()
    if items:
        for item in items:
            item.logo_data = base64.b64encode(item.img).decode('utf-8') if item.img else None
            total_price += item.price
    return render_template('cart.html', title='Корзина', items=items, total_price=total_price)


# Удаление товара из корзины
@app.route('/delete_from_cart/<int:id>')
@login_required
def delete_from_cart(id):
    db_sess = get_db_session()
    user: User = db_sess.query(User).get(current_user.id)
    if user:
        user.shopping_cart = user.shopping_cart.replace(f",{id}", '')
        sp = user.shopping_cart.split(',')
        if f'{id}' in sp:
            sp.remove(f'{id}')
            user.shopping_cart = ','.join(sp)
        db_sess.commit()
    return redirect(url_for('cart'))