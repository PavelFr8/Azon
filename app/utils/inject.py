from flask_login import current_user

from app.models import Shop, Category

def inject():
    """
    shops и categories теперь типо глобальная переменная для жижи
    :return: dict
    """
    if current_user.is_authenticated:
        shops = Shop.query.filter_by(owner_id=current_user.id).all()
    else:
        shops = []
    return dict(shops=shops)
