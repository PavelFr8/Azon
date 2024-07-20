from app.models import Category
from app import db
from sqlalchemy import text

categories = [
    'Без категории', 'Мужская одежда', 'Женская одежда', 'Детская одежда', 'Обувь',
    'Аксессуары', 'Электроника', 'Техника для дома', 'Мебель',
    'Посуда и кухонные принадлежности', 'Бытовая химия', 'Красота и уход',
    'Спорт и фитнес', 'Книги и учебники', 'Игрушки и игры', 'Строительство и материалы',
    'Сад и огород', 'Для животных'
]

def load_categories():
    db.session.execute(text("DELETE FROM categories;"))
    for name in categories:
        category = Category(name=name)
        db.session.add(category)
    db.session.commit()
