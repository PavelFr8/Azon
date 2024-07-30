from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

import sqlalchemy as sa
import sqlalchemy.orm as orm

import datetime
import base64

from app import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    email = sa.Column(sa.String, unique=True, nullable=False, index=True)
    hashed_password = sa.Column(sa.String, nullable=False)
    address = sa.Column(sa.String, nullable=False, default="Не указан")
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now)

    shop = orm.relationship('Shop', back_populates='user')
    cart = orm.relationship('ShoppingCart', back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def update_password(self, new_password):
        self.set_password(new_password)

    def get_items_in_cart(self):
        items = []
        shopping_carts = ShoppingCart.query.filter_by(user_id=self.id).all()
        for cart in shopping_carts:
            item: Item = Item.query.get(cart.item_id)
            item.logo_data = base64.b64encode(item.img).decode('utf-8') if item.img else None
            item.amount = cart.amount
            items.append(item)
        return items


class Item(db.Model):
    __tablename__ = 'items'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    article = sa.Column(sa.BigInteger, nullable=False, unique=True)
    name = sa.Column(sa.String, nullable=False)
    price = sa.Column(sa.Integer, nullable=False)
    about = sa.Column(sa.String, nullable=False)
    img = sa.Column(sa.LargeBinary, nullable=False)
    category_id = sa.Column(sa.String, nullable=False)
    seller_id = sa.Column(sa.Integer, sa.ForeignKey("shops.id"))
    comments = sa.Column(sa.JSON, nullable=True)
    rating = sa.Column(sa.String, nullable=True, default="0;0;0")

    shop = orm.relationship('Shop')
    cart = orm.relationship("ShoppingCart", back_populates="item")


class Shop(db.Model):
    __tablename__ = 'shops'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False, unique=True)
    about = sa.Column(sa.Text, nullable=True, default='Описание магазина')
    img = sa.Column(sa.LargeBinary, nullable=False)
    contact = sa.Column(sa.String, nullable=True)
    owner_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))

    items = orm.relationship('Item', back_populates='shop')
    user = orm.relationship('User')


class Category(db.Model):
    __tablename__ = 'categories'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False, unique=True)


class ShoppingCart(db.Model):
    __tablename__ = 'carts'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False)
    item_id = sa.Column(sa.Integer, sa.ForeignKey("items.id"), nullable=False)
    amount = sa.Column(sa.Integer, nullable=False)

    user = orm.relationship("User")
    item = orm.relationship("Item")
