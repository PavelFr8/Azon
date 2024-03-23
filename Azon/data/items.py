from .db_session import SqlAlchemyBase
import sqlalchemy as sa
import sqlalchemy.orm as orm


class Item(SqlAlchemyBase):
    __tablename__ = 'items'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    price = sa.Column(sa.Integer, nullable=False)
    about = sa.Column(sa.String, nullable=False)
    img = sa.Column(sa.LargeBinary, nullable=False)
    category1 = sa.Column(sa.Integer, sa.ForeignKey("categories.id"), nullable=False)
    category2 = sa.Column(sa.Integer, sa.ForeignKey("categories.id"), nullable=True)
    category3 = sa.Column(sa.Integer, sa.ForeignKey("categories.id"), nullable=True)
    seller_id = sa.Column(sa.Integer, sa.ForeignKey("shops.id"))

    shop = orm.relationship('Shop')
    categories = orm.relationship('Category')