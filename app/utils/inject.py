from flask_login import current_user

from app.models import Shop, Category

def inject():
    """
    shops now global for Jinja2
    :return: dict
    """
    if current_user.is_authenticated:
        shops = Shop.query.filter_by(owner_id=current_user.id).all()
    else:
        shops = []
    return dict(shops=shops)
