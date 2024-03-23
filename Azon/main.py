from flask import Flask, render_template, redirect, request, abort
from data.allowes_file import allowed_file
from data import db_session
from data.users import User
from data.shops import Shop
from data.items import Item
from forms.registerform import RegisterForm
from forms.shopform import ShopForm
from forms.loginform import LoginForm
from forms.userchange import UserChangeForm
from forms.shopchange import ShopChangeForm
from forms.itemform import ItemForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'q2345rtghji98765e'
# app.config['DEBUG'] = True

login_manager = LoginManager()
login_manager.init_app(app)


# shops теперь типо глобальная переменная для жижи
@app.context_processor
def inject_shops():
    if current_user.is_authenticated:
        sess = db_session.create_session()
        shops = sess.query(Shop).filter(Shop.owner_id == current_user.id).all()
    else:
        shops = []
    return dict(shops=shops)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


# Главная страница
@app.route('/')
def index():
    return render_template("index.html", title='Azon')


# Страница "Стать продавцом"
@app.route('/shop/about')
@login_required
def shop_about():
    return render_template('shop-about.html', title='Стать продавцом')


# Страница "О нас"
@app.route('/about')
def about():
    return render_template('about.html', title='О нас')


#              !!!!! БЛОК СВЯЗАННЫЙ С ПОЛЬЗОВАТЕЛЕМ !!!!!

# Регистрация пользователя
@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message='Пароли не совпадают!')
        db_sess = db_session.create_session()
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
        db_sess = db_session.create_session()
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
    db_sess = db_session.create_session()
    user: User = db_sess.query(User).get(current_user.id)
    return render_template('profile.html', user=user, title='Ваш профиль')


# Обновление пароля аккаунта
@app.route('/user/<int:id>', methods=['GET', 'POST'])
@login_required
def user_change(id: int):
    form = UserChangeForm()
    if request.method == 'GET':
        db_sess = db_session.create_session()
        user: User = db_sess.query(User).filter(User.id == id, current_user.id == id).first()
        if user:
            form.email.data = user.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
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
        db_sess = db_session.create_session()
        if db_sess.query(Shop).filter(Shop.name == form.name.data).first():
            return render_template('shop-register.html', title='Регистрация', form=form,
                                   message='Магазин с таким названием уже существует')
        img_file = request.files['img']
        if img_file and allowed_file(img_file.filename):  # проверка, что файл является фото
            img_binary = img_file.read()
            db_sess = db_session.create_session()
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
@login_required
def shop_profile(id):
    db_sess = db_session.create_session()
    shop = db_sess.query(Shop).filter(Shop.id == id, Shop.owner_id == current_user.id).first()

    # Преобразуем бинарные данные логотипа в base64
    logo_data = base64.b64encode(shop.img).decode('utf-8')

    return render_template('shop-profile.html', shop=shop, title=f'Профиль магазина "{shop.name}"', logo_data=logo_data)


# Редактирование данных о магазине
@app.route('/shop/<int:id>', methods=['GET', 'POST'])
@login_required
def shop_change(id: int):
    form = ShopChangeForm()
    if request.method == 'GET':
        db_sess = db_session.create_session()
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
        db_sess = db_session.create_session()
        shop = db_sess.query(Shop).filter(Shop.id == id, Shop.owner_id == current_user.id).first()
        img_file = request.files['img']
        if shop:
            if img_file and allowed_file(img_file.filename):   # проверка, что файл является фото
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
@app.route('/itemregister', methods=['POST', 'GET'])
@login_required
def item_register():
    form = ItemForm()
    if form.validate_on_submit():
        img_file = request.files['img']
        if img_file and allowed_file(img_file.filename):  # проверка, что файл является фото
            img_binary = img_file.read()
            db_sess = db_session.create_session()
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
'''

# Редактирование данных о магазине
@app.route('/shop/<int:id>', methods=['GET', 'POST'])
@login_required
def shop_change(id: int):
    form = ShopChangeForm()
    if request.method == 'GET':
        db_sess = db_session.create_session()
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
        db_sess = db_session.create_session()
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
'''

if __name__ == '__main__':
    db_session.global_init('db/db.db')
    app.run(port='8080', host='127.0.0.1')
