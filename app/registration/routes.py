from flask import render_template, make_response, redirect
from flask_login import login_user, login_required, logout_user

import base64

from app.models import User, Item, Shop, Category
from app import db
from . import module
from .forms import RegisterForm, LoginForm


# Регистрация пользователя
@module.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registration/register.html', title='Регистрация', form=form,
                                   message='Пароли не совпадают!')
        if User.query.filter_by(email=form.email.data).first():
            return render_template('registration/register.html', title='Регистрация', form=form,
                                   message='Такой пользователь уже есть')
        user = User(
            email=form.email.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        return redirect('/login/login')

    return render_template('registration/register.html', title='Регистрация', form=form)


# Логин
@module.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user: User = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)

            # Сохраняем куки
            if form.remember_me.data:
                response = make_response(redirect('/'))
                response.set_cookie('username', user.email, max_age=60*60*24*365, httponly=True, secure=True)
                return response
            else:
                return redirect('/')

        return render_template('registration/login.html', title='Авторизация', message='Неверный логин или пароль', form=form)
    return render_template('registration/login.html', title='Авторизация', form=form)


# Выход из аккаунта
@module.route('/logout')
@login_required
def logout():
    logout_user()

    # Удаляем куки
    response = make_response(redirect('/'))
    response.set_cookie('username', '', expires=0)
    return response