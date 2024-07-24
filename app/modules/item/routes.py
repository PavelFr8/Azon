from flask import request, render_template, abort, redirect, url_for, flash
from flask_login import login_required, current_user

import base64

from app.models import Item, Shop, Category, User
from app import db, logger
from app.utils.allowed_file import allowed_file
from . import module
from .forms import ItemForm, CommentForm


# Регистрация нового товара
@module.route('/register/<string:shop_name>', methods=['POST', 'GET'])
@login_required
def register(shop_name):
    form = ItemForm()
    if form.validate_on_submit():
        img_file = request.files['img']
        if img_file and allowed_file(img_file.filename):
            try:
                img_binary = img_file.read()
                categories = [form.category1.data, form.category2.data, form.category3.data]
                category_ids = []
                for category in categories:
                    ctgr = Category.query.filter_by(name=category).first()
                    if ctgr and ctgr.id not in category_ids:
                        category_ids.append(ctgr.id)
                shop = Shop.query.filter_by(name=shop_name, owner_id=current_user.id).first()
                item = Item(
                    name=form.name.data,
                    price=form.price.data,
                    about=form.about.data,
                    img=img_binary,
                    category_id=','.join(map(str, category_ids)),
                    seller_id=shop.id
                )
                db.session.add(item)
                db.session.commit()
                flash('Товар успешно зарегистрирован!', 'success')
                return redirect('/')
            except Exception as e:
                logger.error(f"Error registering item: {e}")
                db.session.rollback()
                flash("Произошла ошибка при регистрации товара.", 'danger')
        else:
            return render_template('item/item-register.html',
                                   title='Добавление нового товара',
                                   message='Недопустимое расширение файла изображения. Разрешены только PNG, JPG и JPEG'
                                   , form=form, item=None)
    return render_template('item/item-register.html', title='Добавление нового товара', form=form, item=None)


# Профиль товара
@module.route('/profile/<int:id>')
def profile(id):
    form = CommentForm()
    try:
        item = Item.query.get(id)
        if not item:
            abort(404)

        shop: Shop = Shop.query.get(item.seller_id)
        comments = item.comments.split(';') if item.comments else []

        logo_data = base64.b64encode(item.img).decode('utf-8') if item.img else None
        logo_data2 = base64.b64encode(shop.img).decode('utf-8') if shop.img else None

        return render_template('item/item-profile.html', item=item, title=f'{item.name}', logo_data=logo_data,
                               comments=comments, form=form, logo_data2=logo_data2)
    except Exception as e:
        logger.error(f"Error loading item profile: {e}")
        flash("Произошла ошибка при загрузке профиля товара.", 'danger')
        return redirect(url_for('menu.index'))

# Обработчик для отправки отзывов
@module.route('/add_comment/<int:id>', methods=['POST'])
@login_required
def add_comment(id):
    form = CommentForm(request.form)
    if form.validate_on_submit() and 'rate' in request.form:
        try:
            item: Item = db.session.get(Item, id)
            if not item:
                abort(404)

            current_rating = item.rating
            if current_rating:
                sum_rating = int(current_rating.split(';')[0])
                num_rating = int(current_rating.split(';')[1])
            else:
                sum_rating, num_rating, average_rating = 0, 0, 0

            sum_rating += int(request.form['rate'])
            num_rating += 1
            average_rating = round(sum_rating / num_rating, 1)
            item.rating = f"{sum_rating};{num_rating};{average_rating}"

            if item.comments:
                item.comments += f";{form.text.data}"
            else:
                item.comments = form.text.data

            db.session.commit()
            flash("Ваш отзыв успешно добавлен!", 'success')
        except Exception as e:
            logger.error(f"Error adding comment: {e}")
            db.session.rollback()
            flash("Произошла ошибка при добавлении отзыва.", 'danger')

    return redirect(url_for('item.profile', id=id))

# Удаление товара
@module.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    try:
        item: Item = Item.query.get(id)
        if not item:
            abort(404)

        # Удаляем товар из корзины каждого пользователя, у которого он есть
        users_with_item = User.query.filter(User.shopping_cart.like(f"%{item.id}%"))
        for user in users_with_item:
            user.shopping_cart = ','.join(filter(lambda x: x != str(item.id), user.shopping_cart.split(',')))

        db.session.delete(item)
        db.session.commit()
        flash("Товар успешно удален!", 'success')
        return redirect(url_for('shop.profile', id=item.seller_id if item else 0))
    except Exception as e:
        logger.error(f"Error deleting item: {e}")
        db.session.rollback()
        flash("Произошла ошибка при удалении товара.", 'danger')


# Изменение данных о товаре
@module.route('/change/<int:id>', methods=['GET', 'POST'])
@login_required
def change(id):
    form = ItemForm()
    try:
        item = Item.query.filter_by(id=id).first()
        if not item:
            abort(404)

        if request.method == 'GET':
            logo_data = base64.b64encode(item.img).decode('utf-8') if item.img else None

            categories = item.category_id.split(',')
            ctgr = [Category.query.get(int(category_id)) for category_id in categories if Category.query.get(int(category_id))]

            form.name.data = item.name
            form.price.data = item.price
            form.about.data = item.about
            form.category1.data = ctgr[0].name if ctgr else ''
            form.category2.data = ctgr[1].name if len(ctgr) > 1 else ''
            form.category3.data = ctgr[2].name if len(ctgr) > 2 else ''

            return render_template('item/item-register.html', title='Изменение данных', form=form, item=item, logo_data=logo_data)

        if form.validate_on_submit():
            img_file = request.files['img']
            if img_file and img_file.filename != '':
                if not allowed_file(img_file.filename):
                    return render_template('item/item-register.html',
                                           title='Изменение данных',
                                           message='Недопустимое расширение файла изображения. Разрешены только PNG, JPG и JPEG',
                                           form=form,
                                           item=item)
                img_binary = img_file.read()
                item.img = img_binary

            categories = [form.category1.data, form.category2.data, form.category3.data]
            category_ids = []
            for category in categories:
                ctgr = Category.query.filter(Category.name == category).first()
                if ctgr:
                    category_ids.append(ctgr.id)

            item.name = form.name.data
            item.about = form.about.data
            item.price = form.price.data
            item.category_id = ','.join(map(str, category_ids))
            db.session.commit()
            flash("Данные о товаре успешно обновлены!", 'success')
            return redirect(url_for('item.profile', id=id))
        return render_template('item/item-register.html', title='Изменение данных', form=form, item=item)

    except Exception as e:
        logger.error(f"Error updating item: {e}")
        db.session.rollback()
        flash("Произошла ошибка при обновлении данных о товаре.", 'danger')
