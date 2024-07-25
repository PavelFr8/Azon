from flask import request, render_template, redirect, url_for, flash
from flask_login import current_user, login_required

import base64

from app.models import Item, Shop
from app import db, logger
from app.utils.allowed_file import allowed_file
from . import module
from .forms import ShopRegisterForm, ShopChangeInfoForm


# Регистрация нового магазина
@module.route('/register', methods=['POST', 'GET'])
@login_required
def register():
    form = ShopRegisterForm()
    if form.validate_on_submit():
        if Shop.query.filter_by(name=form.name.data).first():
            return render_template('shop/shop-register.html', title='Регистрация', form=form,
                                   message='Магазин с таким названием уже существует')

        img_file = request.files['img']
        if img_file and allowed_file(img_file.filename):  # проверка, что файл является фото
            try:
                img_binary = img_file.read()
                shop = Shop(
                    name=form.name.data,
                    about=form.about.data,
                    img=img_binary,
                    owner_id=current_user.id,
                    contact=current_user.email
                )
                db.session.add(shop)
                db.session.commit()
                flash('Магазин успешно зарегистрирован!', 'success')
                return redirect(url_for('menu.index'))
            except Exception as e:
                logger.error(f"Error registering shop: {e}")
                db.session.rollback()
                flash('Произошла ошибка при регистрации магазина.', 'danger')
        else:
            return render_template('shop/shop-register.html',
                                   title='Регистрация магазина',
                                   message='Недопустимое расширение файла изображения. Разрешены только PNG, JPG и JPEG'
                                   , form=form)
    return render_template('shop/shop-register.html', title='Регистрация магазина', form=form)


# Профиль магазина
@module.route('/profile/<string:shop_name>')
def profile(shop_name):
    shop = Shop.query.filter_by(name=shop_name).first_or_404()
    items = Item.query.filter_by(seller_id=shop.id).all()

    logo_data = base64.b64encode(shop.img).decode('utf-8')  # Преобразуем бинарные данные логотипа в base64
    for item in items:
        item.logo_data = base64.b64encode(item.img).decode('utf-8') if item.img else None

    return render_template('shop/shop-profile.html', shop=shop, items=items, title=f'Профиль магазина "{shop.name}"',
                           logo_data=logo_data)


# Редактирование данных о магазине
@module.route('change/<string:shop_name>', methods=['GET', 'POST'])
@login_required
def change_info(shop_name):
    form = ShopChangeInfoForm()
    try:
        shop = Shop.query.filter_by(name=shop_name, owner_id=current_user.id).first_or_404()
        if request.method == 'GET':
            logo_data = base64.b64encode(shop.img).decode('utf-8') if shop.img else None
            form.name.data = shop.name
            form.about.data = shop.about
            form.contact.data = shop.contact
            return render_template('shop/shop-info-change.html', title='Изменение данных', form=form, shop=shop,
                                   logo_data=logo_data)
        if form.validate_on_submit():
            img_file = request.files['img']
            if img_file and img_file.filename != '':
                if not allowed_file(img_file.filename):
                    return render_template('shop-change.html',
                                           title='Изменение данных',
                                           message='Недопустимое расширение файла изображения. Разрешены только '
                                                   'PNG, JPG и JPEG',
                                           form=form, shop=shop)
                img_binary = img_file.read()
                shop.img = img_binary
            shop.name = form.name.data
            shop.about = form.about.data
            shop.contact = form.contact.data

            db.session.commit()
            flash('Данные магазина успешно обновлены!', 'success')
            return redirect(url_for('shop.profile', shop_name=shop.name))

    except Exception as e:
        logger.error(f"Error updating shop info: {e}")
        db.session.rollback()
        flash('Произошла ошибка при обновлении данных магазина.', 'danger')
