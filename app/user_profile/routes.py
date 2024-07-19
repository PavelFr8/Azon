from flask import request, render_template, abort, redirect, url_for
from flask_login import current_user, login_required

import base64

from app.models import User, Item
from app import db
from . import module
from .forms import UserChangePasswordForm


# Личный профиль пользователя
@module.route('/profile')
@login_required
def profile():
    user: User = User.query.get(current_user.id)
    items_in_cart = []
    items = []
    if current_user.shopping_cart:
        items_in_cart = [int(id) for id in current_user.shopping_cart.split(',') if id]
    if items_in_cart:
        items = Item.query.filter_by(Item.id.in_(items_in_cart)).all()
    if items:
        for item in items:
            item.logo_data = base64.b64encode(item.img).decode('utf-8') if item.img else None
    return render_template('user_profile/profile.html', user=user, title='Ваш профиль', items=items)


# Обновление пароля аккаунта
@module.route('/change_password/<int:id>', methods=['GET', 'POST'])
@login_required
def change_password(id: int):
    form = UserChangePasswordForm()
    if request.method == 'GET':
        user: User = User.query.filter(id == id, current_user.id == id).first()
        if user:
            form.email.data = user.email
        else:
            abort(404)
    if form.validate_on_submit():
        user: User = User.query.filter(id == id, current_user.id == id).first()
        if user:
            if user.check_password(form.curr_password.data):
                user.set_password(form.new_password.data)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('profile'))
            else:
                form.email.data = user.email
                return render_template('user_profile/change_password.html', title='Ваш профиль', form=form, message='Неверный пароль')
        else:
            abort(404)

    return render_template('user_profile/change_password.html', title='Ваш профиль', form=form)
