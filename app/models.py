from app import db
import sqlalchemy as sa
import sqlalchemy.orm as orm
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    email = sa.Column(sa.String, unique=True, nullable=False, index=True)
    hashed_password = sa.Column(sa.String, nullable=False)
    shopping_cart = sa.Column(sa.String, nullable=True)
    delivery_address = sa.Column(sa.String, nullable=True)  # тут пустота true но надо будеть сделать false
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now)
    address = sa.Column(sa.String, nullable=True, default='Не выбран')

    shop = orm.relationship('Shop', back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def update_password(self, new_password):
        self.set_password(new_password)


class Item(db.Model):
    __tablename__ = 'items'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    price = sa.Column(sa.Integer, nullable=False)
    about = sa.Column(sa.String, nullable=False)
    img = sa.Column(sa.LargeBinary, nullable=False)
    category_id = sa.Column(sa.String, nullable=False)
    seller_id = sa.Column(sa.Integer, sa.ForeignKey("shops.id"))
    comments = sa.Column(sa.String, nullable=True)
    rating = sa.Column(sa.String, nullable=True, default="0;0;0")

    shop = orm.relationship('Shop')


class Shop(db.Model):
    __tablename__ = 'shops'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False, unique=True)
    about = sa.Column(sa.String, nullable=True, default='Описание магазина')
    img = sa.Column(sa.LargeBinary, nullable=False)
    contact = sa.Column(sa.String, nullable=True)
    owner_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))

    items = orm.relationship('Item', back_populates='shop')
    user = orm.relationship('User')


class Category(db.Model):
    __tablename__ = 'categories'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
