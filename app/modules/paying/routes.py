from flask import flash, render_template, redirect, url_for
from flask_login import login_required, current_user

from app.models import User, ShoppingCart
from app import db, logger
from . import module
from .forms import BuyForm


# Paying for items in shopping cart
@module.route('/card', methods=['GET', 'POST'])
@login_required
def buy():
    form = BuyForm()
    total_price = 0
    try:
        user: User = User.query.get_or_404(current_user.id)
        items = user.get_items_in_cart()
        for item in items:
            total_price += item.price * item.amount
        if form.validate_on_submit():
            if user.address != 'Не выбран':
                items_in_cart: ShoppingCart = ShoppingCart.query.filter_by(user_id=current_user.id).all()
                for item in items_in_cart:
                    db.session.delete(item)
                db.session.commit()
                flash('Успешная оплата!', 'success')
                return redirect(url_for('menu.index'))
            else:
                db.session.rollback()
                flash("Адрес доставки не указан", "danger")
                return redirect(url_for('location.address'))
    except Exception as e:
        logger.error(f"Error while paying: {e}")
        flash("Ошибка при оплате", "danger")
        return redirect(url_for('menu.index'))

    return render_template('paying/buy.html', title='Оплата', total_price=total_price, form=form)
