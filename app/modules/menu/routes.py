from flask import request, render_template, abort
from flask_login import current_user, login_user

import base64

from app.models import User, Item, Shop, Category
from . import module


# Main page
@module.route('/')
def index():
    items = Item.query.all()
    for item in items:
        item.logo_data = base64.b64encode(item.img).decode('utf-8') if item.img else None
    categories = Category.query.all()[1:]
    return render_template("item.html", title='Azon', items=items, categories=categories)


# Page "Стать продавцом"
@module.route('/info')
def info():
    return render_template('menu/become_a_seller.html', title='Программа продавцов')


# Page "О нас"
@module.route('/about')
def about():
    return render_template('menu/about.html', title='О нас')


# Page "Категории"
@module.route('/categories')
def categories():
    categories = Category.query.all()[1:]
    return render_template('menu/category.html', title='Категории', categors=categories)


# Page "Продавцы"
@module.route('/shops')
def shops():
    shops = Shop.query.all()
    for shop in shops:
        shop.logo_data = base64.b64encode(shop.img).decode('utf-8') if shop.img else None
    return render_template('menu/shops.html', title='Продавцы', shops=shops)


# searching item
@module.route('/search')
def search_item():
    query = request.args.get('query')  # get 'query'
    if query:
        items = Item.query.filter(Item.name.ilike(f'%{query}%')).all()  # search by name
        if not items:
            items = Item.query.filter(Item.article == query).all() # search by article
    else:
        items = Item.query.all()
    for item in items:
        item.logo_data = base64.b64encode(item.img).decode('utf-8') if item.img else None
    if query == '':
        categories = Category.query.all()[1:]
        return render_template("item.html", title='Результаты поиска', items=items, text=query, categories=categories)
    else:
        return render_template("item.html", title='Результаты поиска', items=items, text=query)


# Get items from category
@module.route('/categories/<string:category_name>')
def items_by_category(category_name):
    category = Category.query.filter_by(name=category_name).first()
    if not category:
        abort(404)

    items = Item.query.filter(Item.category_id.ilike(f'%{category.id}%')).all()
    for item in items:
        item.logo_data = base64.b64encode(item.img).decode('utf-8') if item.img else None

    return render_template('item.html', title=f'Товары в категории {category.name}', items=items, name=category.name)
