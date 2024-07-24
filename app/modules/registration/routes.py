from flask import render_template, make_response, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user

from app.models import User
from app import db, logger
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

        try:
            user = User(email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Регистрация прошла успешно!', 'success')
            return redirect(url_for('registration.login'))
        except Exception as e:
            logger.error(f"Error registering user: {e}")
            db.session.rollback()
            return render_template('registration/register.html', title='Регистрация', form=form,
                                   message='Произошла ошибка при регистрации.')

    return render_template('registration/register.html', title='Регистрация', form=form)


# Логин
@module.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)

                response = make_response(redirect(url_for('menu.index')))
                if form.remember_me.data:
                    response.set_cookie('username', user.email, max_age=60*60*24*365, httponly=True, secure=True,
                                        samesite='Lax')
                else:
                    response.set_cookie('username', '', expires=0)
                flash('Вы успешно вошли!', 'success')
                return response

            return render_template('registration/login.html', title='Авторизация', message='Неверный логин или пароль',
                                   form=form)
        except Exception as e:
            logger.error(f"Error during login: {e}")
            return render_template('registration/login.html', title='Авторизация', form=form,
                                   message='Произошла ошибка при авторизации.')

    return render_template('registration/login.html', title='Авторизация', form=form)


# Выход из аккаунта
@module.route('/logout')
@login_required
def logout():
    logout_user()
    response = make_response(redirect(url_for('menu.index')))
    response.set_cookie('username', '', expires=0)

    return response
