from flask import request, render_template, abort
from flask_login import current_user, login_user

import base64

from app.models import User, Item, Shop, Category
from . import module


# Главная страница
@module.route('/')
def index():
    # Проверяем куки
    username = request.cookies.get('username')
    if username and not current_user.is_authenticated:
        user = User.query.filter_by(email=username).first()
        if user:
            login_user(user)
    items = Item.query.all()
    for item in items:
        item.logo_data = base64.b64encode(item.img).decode('utf-8') if item.img else None
    categories = Category.query.all()[1:]
    return render_template("item.html", title='Azon', items=items, categories=categories)


# Страница "Стать продавцом"
@module.route('/info')
def info():
    return render_template('menu/become_a_seller.html', title='Программа продавцов')


# Страница "О нас"
@module.route('/about')
def about():
    return render_template('menu/about.html', title='О нас')


# Страница "Категории"
@module.route('/categories')
def categories():
    categories = Category.query.all()[1:]
    return render_template('menu/category.html', title='Категории', categors=categories)


# Страница "Продавцы"
@module.route('/shops')
def shops():
    shops = Shop.query.all()
    for shop in shops:
        shop.logo_data = base64.b64encode(shop.img).decode('utf-8') if shop.img else None
    return render_template('menu/shops.html', title='Продавцы', shops=shops)


# Поиск по имени товара
@module.route('/search')
def search_item():
    query = request.args.get('query')  # Получаем значение запроса из параметра 'query'
    if query:
        items = Item.query.filter(Item.name.ilike(f'%{query}%')).all()  # Ищем товары по названию
    else:
        items = Item.query.all()  # Ищем все товары
    for item in items:
        item.logo_data = base64.b64encode(item.img).decode('utf-8') if item.img else None
    if query == '':
        categories = Category.query.all()[1:]
        return render_template("item.html", title='Результаты поиска', items=items, text=query, categories=categories)
    else:
        return render_template("item.html", title='Результаты поиска', items=items, text=query)


# Отображение товаров по выбранной категории
@module.route('/categories/<string:category_name>')
def items_by_category(category_name):
    category = Category.query.filter_by(name=category_name).first()
    if not category:
        abort(404)

    items = Item.query.filter(Item.category_id.ilike(f'%{category.id}%')).all()
    for item in items:
        item.logo_data = base64.b64encode(item.img).decode('utf-8') if item.img else None

    return render_template('item.html', title=f'Товары в категории {category.name}', items=items, name=category.name)
