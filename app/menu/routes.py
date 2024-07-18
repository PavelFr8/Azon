from flask import request, render_template
from flask_login import current_user, login_user, login_required

import base64

from app.models import User, Item, Shop, Category
from app import login_manager
from . import module


# настройка передачи залогиненных пользователей
@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    if user:
        return user
    # Проверяем куки
    username = request.cookies.get('username')
    if username:
        user = User.query.filter_by(email=username).first()
        if user:
            login_user(user)
            return user


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
    return render_template("item.html", title='Azon', items=items)



# Страница "Стать продавцом"
@module.route('/info')
@login_required
def info():
    return render_template('menu/info.html', title='Программа продавцов')


# Страница "О нас"
@module.route('/about')
def about():
    return render_template('menu/about.html', title='О нас')


# Страница "Категории"
@module.route('/categories')
def categories():
    categories = Category.query.all()[1:]
    return render_template('menu/category.html', title='Категории', categories=categories)


# Страница "Продавцы"
@module.route('/sellers')
def shops():
    shops = Shop.query.all()
    for shop in shops:
        shop.logo_data = base64.b64encode(shop.img).decode('utf-8') if shop.img else None
    return render_template('menu/sellers.html', title='Продавцы', shops=shops)


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

    return render_template("item.html", title='Результаты поиска', items=items, text=query)
