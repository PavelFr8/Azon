from flask import request, render_template, flash, redirect, url_for
from flask_login import current_user, login_required

import base64

from app.models import Item, User, ShoppingCart
from app import db, logger
from . import module
from .forms import UserChangePasswordForm


# Личный профиль пользователя
@module.route('/profile')
@login_required
def profile():
    items = current_user.get_items_in_cart()
    return render_template('user_profile/profile.html', user=current_user, title='Ваш профиль', items=items)


# Обновление пароля аккаунта
@module.route('/change_password/<int:id>', methods=['GET', 'POST'])
@login_required
def change_password(id: int):
    form = UserChangePasswordForm()
    try:
        user: User = current_user
        if request.method == 'GET':
            form.email.data = user.email

        elif form.validate_on_submit():
            if user.check_password(form.curr_password.data):
                user.set_password(form.new_password.data)
                db.session.commit()
                flash('Пароль успешно изменен!', 'success')
                return redirect(url_for('user_profile.profile'))
            else:
                form.email.data = user.email
                flash('Неверный текущий пароль', 'warning')

    except Exception as e:
        logger.error(f"Error changing password for user {id}: {e}")
        db.session.rollback()
        flash('Произошла ошибка при изменении пароля.', 'danger')

    return render_template('user_profile/change_password.html', title='Ваш профиль', form=form)
