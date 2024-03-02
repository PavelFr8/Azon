from .db_session import SqlAlchemyBase
import sqlalchemy as sa
import sqlalchemy.orm as orm
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=True)
    hashed_password = sa.Column(sa.String, nullable=True)
    email = sa.Column(sa.String, unique=True, nullable=True, index=True)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now)

    def __repr__(self) -> str:
        return f'<{self.id}> {self.name} {self.email}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
