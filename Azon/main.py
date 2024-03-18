from flask import Flask, render_template, redirect, request, make_response, session, abort
from werkzeug.utils import secure_filename
from data.allowes_file import allowed_file
from data import db_session
from data.users import User
from data.shops import Shop
from forms.registerform import RegisterForm
from forms.shopform import ShopForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms.loginform import LoginForm
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandex_123'
# app.config['DEBUG'] = True

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    return render_template("index.html", title='Azon')


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


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/shop/about')
@login_required
def shop_about():
    return render_template('shop-about.html', title='Стать продавцом')


@app.route('/shopregister', methods=['POST', 'GET'])
@login_required
def shop_register():
    form = ShopForm()
    if form.validate_on_submit():
        img_file = request.files['img']
        if img_file and allowed_file(img_file.filename):
            img_binary = img_file.read()
            db_sess = db_session.create_session()
            shop = Shop(
                name=form.name.data,
                about=form.about.data,
                img=img_binary,
                owner_id=current_user.id
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


if __name__ == '__main__':
    db_session.global_init('db/db.db')
    app.run(port='8080', host='127.0.0.1')
