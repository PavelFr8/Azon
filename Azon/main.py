from flask import Flask, render_template, redirect, request, abort, url_for, g
from data.allowes_file import allowed_file
from data.category_loader import load_categories
from data.get_db_session import get_db_session
from data import db_session
from data.users import User
from data.shops import Shop
from data.items import Item
from data.categories import Category
from forms.registerform import RegisterForm
from forms.shopform import ShopForm
from forms.loginform import LoginForm
from forms.userchange import UserChangeForm
from forms.shopchange import ShopChangeForm
from forms.itemform import ItemForm
from forms.commentform import CommentForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'q2345rtghji98765e'
# app.config['DEBUG'] = True

login_manager = LoginManager()
login_manager.init_app(app)


# shops и categories теперь типо глобальная переменная для жижи
@app.context_processor
def inject_shops():
    sess = get_db_session()  # Используем функцию для получения сессии
    if current_user.is_authenticated:
        shops = sess.query(Shop).filter(Shop.owner_id == current_user.id).all()
        categories = sess.query(Category).all()
    else:
        shops = []
        categories = []
    return dict(shops=shops, categories=categories)


@login_manager.user_loader
def load_user(user_id):
    db_sess = get_db_session()
    return db_sess.query(User).get(user_id)


# Главная страница
@app.route('/')
def index():
    sess = get_db_session()  # Используем функцию для получения сессии
    items = sess.query(Item).all()
    for item in items:
        item.logo_data = base64.b64encode(item.img).decode('utf-8') if item.img else None
    return render_template("item.html", title='Azon', items=items)


# Страница "Стать продавцом"
@app.route('/shop/about')
@login_required
def shop_about():
    return render_template('shop-about.html', title='Программа продавцов')


# Страница "О нас"
@app.route('/about')
def about():
    return render_template('about.html', title='О нас')


# Страница "Категории"
@app.route('/categories')
def categories():
    sess = get_db_session()
    categories = sess.query(Category).all()[1:]
    return render_template('category.html', title='Категории', categories=categories)


# Отображение товаров по выбранной категории
@app.route('/items_by_category/<int:category_id>')
def items_by_category(category_id):
    db_sess = get_db_session()
    category = db_sess.query(Category).get(category_id)
    if not category:
        abort(404)

    items = db_sess.query(Item).filter(Item.category_id.ilike(f'%{category_id}%')).all()
    for item in items:
        item.logo_data = base64.b64encode(item.img).decode('utf-8') if item.img else None

    return render_template('item.html', title=f'Товары в категории {category.name}', items=items)


# Поиск по имени товара
@app.route('/search')
def search_item():
    query = request.args.get('query')  # Получаем значение запроса из параметра 'query'
    sess = get_db_session()
    if query:
        items = sess.query(Item).filter(Item.name.ilike(f'%{query}%')).all()  # Ищем товары по названию
    else:
        items = sess.query(Item).all()  # Ищем все товары
    for item in items:
        item.logo_data = base64.b64encode(item.img).decode('utf-8') if item.img else None

    return render_template("item.html", title='Результаты поиска', items=items, text=query)


#              !!!!! БЛОК СВЯЗАННЫЙ С ПОЛЬЗОВАТЕЛЕМ !!!!!

# Регистрация пользователя
@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message='Пароли не совпадают!')
        db_sess = get_db_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message='Такой пользователь уже есть')
        user = User(
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


# Логин
@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = get_db_session()
        user: User = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html', title='Авторизация', message='Неверный логин или пароль', form=form)
    return render_template('login.html', title='Авторизация', form=form)


# Выход из аккаунта
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


# Личный профиль пользователя
@app.route('/profile')
@login_required
def profile():
    db_sess = get_db_session()
    user: User = db_sess.query(User).get(current_user.id)
    items_in_cart = []
    items = []
    if current_user.shopping_cart:
        items_in_cart = [int(id) for id in current_user.shopping_cart.split(',') if id]
    if items_in_cart:
        items = db_sess.query(Item).filter(Item.id.in_(items_in_cart)).all()
    if items:
        for item in items:
            item.logo_data = base64.b64encode(item.img).decode('utf-8') if item.img else None
    return render_template('profile.html', user=user, title='Ваш профиль', items=items)


# Обновление пароля аккаунта
@app.route('/user/<int:id>', methods=['GET', 'POST'])
@login_required
def user_change(id: int):
    form = UserChangeForm()
    if request.method == 'GET':
        db_sess = get_db_session()
        user: User = db_sess.query(User).filter(User.id == id, current_user.id == id).first()
        if user:
            form.email.data = user.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = get_db_session()
        user: User = db_sess.query(User).filter(User.id == id, current_user.id == id).first()
        if user:
            if user.check_password(form.curr_password.data):
                user.set_password(form.new_password.data)
                db_sess.add(user)
                db_sess.commit()
                return redirect('/profile')
            else:
                form.email.data = user.email
                return render_template('user-change.html', title='Ваш профиль', form=form, message='Неверный пароль')
        else:
            abort(404)

    return render_template('user-change.html', title='Ваш профиль', form=form)


#              !!!!! БЛОК СВЯЗАННЫЙ С МАГАЗИНОМ !!!!!


# Регистрация нового магазина
@app.route('/shopregister', methods=['POST', 'GET'])
@login_required
def shop_register():
    form = ShopForm()
    if form.validate_on_submit():
        db_sess = get_db_session()
        if db_sess.query(Shop).filter(Shop.name == form.name.data).first():
            return render_template('shop-register.html', title='Регистрация', form=form,
                                   message='Магазин с таким названием уже существует')
        img_file = request.files['img']
        if img_file and allowed_file(img_file.filename):  # проверка, что файл является фото
            img_binary = img_file.read()
            db_sess = get_db_session()
            shop = Shop(
                name=form.name.data,
                about=form.about.data,
                img=img_binary,
                owner_id=current_user.id,
                contact=current_user.email
            )
            db_sess.add(shop)
            db_sess.commit()
            return redirect('/')
        else:
            return render_template('shop-register.html',
                                   title='Регистрация магазина',
                                   message='Недопустимое расширение файла изображения. Разрешены только PNG, JPG и JPEG'
                                   , form=form)
    return render_template('shop-register.html', title='Регистрация магазина', form=form)


# Профиль магазина
@app.route('/shop_profile/<int:id>')
def shop_profile(id):
    db_sess = get_db_session()
    shop = db_sess.query(Shop).filter(Shop.id == id).first()
    items = db_sess.query(Item).filter(Item.seller_id == id).all()

    # Преобразуем бинарные данные логотипа в base64
    logo_data = base64.b64encode(shop.img).decode('utf-8')
    for item in items:
        item.logo_data = base64.b64encode(item.img).decode('utf-8') if item.img else None

    return render_template('shop-profile.html', shop=shop, items=items, title=f'Профиль магазина "{shop.name}"',
                           logo_data=logo_data)


# Редактирование данных о магазине
@app.route('/shop/<int:id>', methods=['GET', 'POST'])
@login_required
def shop_change(id: int):
    form = ShopChangeForm()
    if request.method == 'GET':
        db_sess = get_db_session()
        shop = db_sess.query(Shop).filter(Shop.id == id, Shop.owner_id == current_user.id).first()

        # Преобразуем бинарные данные логотипа в base64
        logo_data = base64.b64encode(shop.img).decode('utf-8')
        if shop:
            form.name.data = shop.name
            form.about.data = shop.about
            form.contact.data = shop.contact
            form.img.data = logo_data
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = get_db_session()
        shop = db_sess.query(Shop).filter(Shop.id == id, Shop.owner_id == current_user.id).first()
        img_file = request.files['img']
        if shop:
            if img_file and allowed_file(img_file.filename):  # проверка, что файл является фото
                img_binary = img_file.read()
                shop.name = form.name.data
                shop.about = form.about.data
                shop.contact = form.contact.data
                shop.img = img_binary
                db_sess.commit()
                return redirect(f'/shop_profile/{id}')
            else:
                return render_template('shop-change.html',
                                       title='Изменение данных',
                                       message='Недопустимое расширение файла изображения. Разрешены только '
                                               'PNG, JPG и JPEG'
                                       , form=form)

        else:
            abort(404)

    return render_template('shop-change.html', title='Изменение данных', form=form)


#              !!!!! БЛОК СВЯЗАННЫЙ С ТОВАРАМИ !!!!!


# Регистрация нового товара
@app.route('/itemregister/<int:id>', methods=['POST', 'GET'])
@login_required
def item_register(id):
    form = ItemForm()
    if form.validate_on_submit():
        img_file = request.files['img']
        if img_file and allowed_file(img_file.filename):
            db_sess = get_db_session()
            img_binary = img_file.read()
            categories = [form.category1.data, form.category2.data, form.category3.data]
            category_ids = []
            for category in categories:
                ctgr = db_sess.query(Category).filter(Category.name == category).first()
                if ctgr.id not in category_ids:
                    category_ids.append(ctgr.id)

            item = Item(
                name=form.name.data,
                price=form.price.data,
                about=form.about.data,
                img=img_binary,
                category_id=','.join(map(str, category_ids)),  # Преобразование в строку и объединение ID
                seller_id=id
            )
            db_sess.add(item)
            db_sess.commit()
            return redirect('/')
        else:
            return render_template('item-register.html',
                                   title='Добавление нового товара',
                                   message='Недопустимое расширение файла изображения. Разрешены только PNG, JPG и JPEG'
                                   , form=form)
    return render_template('item-register.html', title='Добавление нового товара', form=form)


# Профиль товара
@app.route('/item_profile/<int:id>')
def item_profile(id):
    form = CommentForm()  # Создаем экземпляр формы
    db_sess = get_db_session()
    item = db_sess.query(Item).filter(Item.id == id).first()
    shop: Shop = db_sess.query(Shop).get(item.seller_id)
    comments = []
    if item.comments:
        comments = item.comments.split(';')

    # Преобразуем бинарные данные логотипа в base64
    logo_data = base64.b64encode(item.img).decode('utf-8')
    logo_data2 = base64.b64encode(shop.img).decode('utf-8')

    # Передаем объект формы в контекст шаблона
    return render_template('item-profile.html', item=item, title=f'{item.name}', logo_data=logo_data,
                           comments=comments, form=form, logo_data2=logo_data2)


# Обработчик для отправки комментария
@app.route('/add_comment/<int:id>', methods=['POST'])
@login_required
def add_comment(id):
    form = CommentForm(request.form)
    if form.validate_on_submit():
        # Если форма валидна, добавляем комментарий к элементу
        db_sess = get_db_session()
        item: Item = db_sess.query(Item).get(id)
        if item:
            # Обновляем поле комментариев у элемента, разделяя их точкой-запятой
            if item.comments:
                item.comments += f";{form.text.data}"
            else:
                item.comments = form.text.data
            db_sess.commit()
        return redirect(url_for('item_profile', id=id))
    return redirect(url_for('item_profile', id=id))


# Удаление товара
@app.route('/delete_item/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_item(id):
    db_sess = get_db_session()
    item: Item = db_sess.query(Item).get(id)
    if item:
        db_sess.delete(item)
        db_sess.commit()
    else:
        abort(404)
    return redirect(f'/shop_profile/{item.seller_id}')


# Изменение данных о товаре
@app.route('/item_change/<int:id>', methods=['GET', 'POST'])
@login_required
def item_change(id: int):
    form = ItemForm()
    db_sess = get_db_session()
    item = db_sess.query(Item).filter(Item.id == id).first()

    if not item:
        abort(404)

    if request.method == 'GET':
        logo_data = base64.b64encode(item.img).decode('utf-8')
        categories = item.category_id.split(',')
        ctgr = []
        for category_id in categories:
            category: Category = db_sess.query(Category).get(int(category_id))
            if category:
                ctgr.append(category)

        form.name.data = item.name
        form.price.data = item.price
        form.about.data = item.about
        form.category1.data = ctgr[0].name if ctgr else ''
        form.category2.data = ctgr[1].name if len(ctgr) > 1 else ''
        form.category3.data = ctgr[2].name if len(ctgr) > 2 else ''
        form.img.data = logo_data

    if form.validate_on_submit():
        img_file = request.files['img']
        if img_file.filename == '':
            return render_template('item-register.html',
                                   title='Изменение данных',
                                   message='Файл изображения не выбран.', form=form)

        if not allowed_file(img_file.filename):
            return render_template('item-register.html',
                                   title='Изменение данных',
                                   message='Недопустимое расширение файла изображения. Разрешены только PNG, JPG и JPEG',
                                   form=form)

        img_binary = img_file.read()
        categories = [form.category1.data, form.category2.data, form.category3.data]
        category_ids = []
        for category in categories:
            ctgr = db_sess.query(Category).filter(Category.name == category).first()
            if ctgr:
                category_ids.append(ctgr.id)

        item.name = form.name.data
        item.about = form.about.data
        item.price = form.price.data
        item.category_id = ','.join(map(str, category_ids))
        item.img = img_binary
        db_sess.commit()
        return redirect(f'/shop_profile/{item.seller_id}')

    return render_template('item-register.html', title='Изменение данных', form=form)


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


if __name__ == '__main__':
    db_session.global_init('db/db.db')
    sess = db_session.create_session()
    categories = sess.query(Category).all()
    if not categories:
        load_categories()  # если категории пропали и с бд беда, то их надо вернуть!
    app.run(port='8080', host='127.0.0.1')
