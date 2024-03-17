from .db_session import SqlAlchemyBase
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy_media import Image, ImageAnalyzer


class Seller(SqlAlchemyBase):
    __tablename__ = 'sellers'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    img = sa.Column(Image.as_mutable(ImageAnalyzer), nullable=True)
    name = sa.Column(sa.String, nullable=False)
    about = sa.Column(sa.String, unique=True, nullable=True, index=True)
    items = sa.Column(sa.String, nullable=True)

    item = orm.relationship('Item', back_populates='seller')