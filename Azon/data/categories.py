from .db_session import SqlAlchemyBase
import sqlalchemy as sa
import sqlalchemy.orm as orm


class Category(SqlAlchemyBase):
    __tablename__ = 'categories'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)

    items = orm.relationship('Item', back_populates='category')