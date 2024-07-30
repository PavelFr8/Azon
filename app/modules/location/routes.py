from flask import request, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError

from .yandex_map_api.get_shops import find_shops
from app.models import User
from app import db, logger
from . import module


@module.route('/address', methods=['GET', 'POST'])
@login_required
def address():
    query = request.args.get('address')
    try:
        closest_shops = find_shops(query)
        if closest_shops == 'Некорректные введённые данные':
            flash('Некорректные введённые данные', 'danger')
    except Exception as e:
        logger.error(f"Error fetching shops: {e}")
        closest_shops = []
        flash('Произошла ошибка при получении данных магазинов', 'danger')

    return render_template('location/address.html',
                           title='Выбор адреса',
                           text=query,
                           closest_shops=closest_shops)


@module.route('/choose/<address>')
@login_required
def choose_address(address):
    try:
        user: User = User.query.get_or_404(current_user.id)
        user.address = address
        db.session.commit()
        flash("Адрес успешно обновлен!", 'success')
    except SQLAlchemyError as e:
        logger.error(f"Error updating user address: {e}")
        db.session.rollback()
        flash("Произошла ошибка при обновлении адреса.", 'danger')
    return redirect(url_for('user_profile.profile'))