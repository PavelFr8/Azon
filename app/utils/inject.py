from flask_login import current_user

from app.models import Shop, Category

# shops и categories теперь типо глобальная переменная для жижи
def inject():
    if current_user.is_authenticated:
        shops = Shop.query.filter_by(owner_id=current_user.id).all()
        categories = Category.query.all()
    else:
        shops = []
        categories = []
    return dict(shops=shops, categories=categories)
