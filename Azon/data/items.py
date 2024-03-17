from .db_session import SqlAlchemyBase
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy_media import Image, ImageAnalyzer


class Item(SqlAlchemyBase):
    __tablename__ = 'items'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    img = sa.Column(Image.as_mutable(ImageAnalyzer), nullable=True)
    seller_id = sa.Column(sa.Integer, sa.ForeignKey("sellers.id"))
    about = sa.Column(sa.String, unique=True, nullable=False, index=True)

    seller = orm.relationship('Seller')