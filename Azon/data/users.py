from .db_session import SqlAlchemyBase
import sqlalchemy as sa
import sqlalchemy.orm as orm
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    email = sa.Column(sa.String, unique=True, nullable=False, index=True)
    hashed_password = sa.Column(sa.String, nullable=False)
    shopping_cart = sa.Column(sa.String, nullable=True)
    delivery_address = sa.Column(sa.String, nullable=True)  # тут пустота true но надо будеть сделать false
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now)
    address = sa.Column(sa.String, nullable=True, default='Не выбран')

    shop = orm.relationship('Shop', back_populates='user')

    def __repr__(self) -> str:
        return f'<{self.id}> {self.email}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def update_password(self, new_password):
        self.set_password(new_password)