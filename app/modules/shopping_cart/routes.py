from flask import render_template
from flask_login import login_required, current_user

from . import module


# Show shopping cart page
@module.route('/')
@login_required
def cart():
    total_price = 0
    items = current_user.get_items_in_cart()
    for item in items:
        total_price += item.price * item.amount
    return render_template('shopping_cart/cart.html', title='Корзина', items=items, total_price=total_price, cart=True)
