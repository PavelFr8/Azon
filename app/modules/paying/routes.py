from flask import request, render_template, abort, redirect, url_for
from flask_login import login_required

import base64

from app.models import Item, Shop, Category, User
from app import db
from app.utils.allowed_file import allowed_file
from . import module
from .forms import BuyForm


# Оплата товара
@app.route('/buy', methods=['GET', 'POST'])
@login_required
def buy():
    form = BuyForm()
    db_sess = get_db_session()
    total_price = 0
    user: User = db_sess.query(User).get(current_user.id)
    total_price = [total_price + item.price for item in db_sess.query(Item).filter(Item.id.in_(
        [int(id) for id in current_user.shopping_cart.split(',') if id])).all()]
    if request.method == 'POST':
        if user.address != 'Не выбран':
            user.shopping_cart = ''
            db_sess.commit()
            return redirect('/')
        return render_template('buy.html', title='Оплата', total_price=total_price[0], form=form,
                               message='Адрес не указан')

    return render_template('buy.html', title='Оплата', total_price=total_price[0], form=form)