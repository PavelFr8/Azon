from flask import Flask, render_template, redirect, request, url_for
from flask_login import LoginManager, login_required, current_user

from func.yandex_map_api.get_shops import find_shops

from app.utils.load_categories import load_categories
from data.get_db_session import get_db_session
from data import db_session
from data.users import User
from data.items import Item
from data.categories import Category

from forms.buyform import BuyForm

import base64
from datetime import timedelta


app = Flask(__name__)
app.config['SECRET_KEY'] = 'q2345rtghji98765e'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365)
# app.config['DEBUG'] = True

login_manager = LoginManager()
login_manager.init_app(app)



#              !!!!! БЛОК СВЯЗАННЫЙ С ПОЛЬЗОВАТЕЛЕМ !!!!!


#              !!!!! БЛОК СВЯЗАННЫЙ С МАГАЗИНОМ !!!!!



#              !!!!! БЛОК СВЯЗАННЫЙ С ТОВАРАМИ !!!!!




#              !!!!! БЛОК СВЯЗАННЫЙ С КОРЗИНОЙ !!!!!

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


#              !!!!! БЛОК СВЯЗАННЫЙ С ОПЛАТОЙ !!!!!


# Оплата товара
@app.route('/buy', methods=['GET', 'POST'])
@login_required
def buy():
    form = BuyForm()
    db_sess = get_db_session()
    total_price = 0
    user: User = db_sess.query(User).get(current_user.id)
    total_price = [total_price + item.price for item in db_sess.query(Item).filter(Item.id.in_(
        [int(id) for id in current_user.shopping_cart.split(',') if id])).all()]
    if request.method == 'POST':
        if user.address != 'Не выбран':
            user.shopping_cart = ''
            db_sess.commit()
            return redirect('/')
        return render_template('buy.html', title='Оплата', total_price=total_price[0], form=form,
                               message='Адрес не указан')

    return render_template('buy.html', title='Оплата', total_price=total_price[0], form=form)


@app.route('/address', methods=['GET', 'POST'])
@login_required
def address():
    query = request.args.get('query')
    closest_shops = find_shops(query)
    if closest_shops == 'Некорректные введённые данные':
        return render_template('address.html', title='Выбор адреса', text=query, closest_shops=closest_shops,
                               message='Некорректные введённые данные')
    return render_template('address.html', title='Выбор адреса', text=query, closest_shops=closest_shops)


@app.route('/choose_address/<address>')
@login_required
def choose_address(address):
    db_sess = get_db_session()
    user: User = db_sess.query(User).get(current_user.id)
    if user:
        user.address = address
        db_sess.commit()
    return redirect('/buy')


if __name__ == '__main__':
    db_session.global_init('db/db.db')
    sess = db_session.create_session()
    categories = sess.query(Category).all()
    if not categories:
        load_categories()  # если категории пропали и с бд беда, то их надо вернуть!
    app.run(port='8080', host='127.0.0.1')
