from app.models import Category
from app import db
from sqlalchemy import text

categories = [
    'Без категории', 'Мужская одежда', 'Женская одежда', 'Детская одежда', 'Обувь',
    'Аксессуары', 'Электроника', 'Мебель', 'Посуда и кухонные принадлежности', 'Бытовая химия', 'Красота и уход',
    'Спорт и фитнес', 'Книги и учебники', 'Игрушки и игры', 'Строительство и материалы', 'Для животных'
]

def load_categories():
    """
    Load categories to database
    """
    try:
        db.session.execute(text("DELETE FROM categories;"))
        for name in categories:
            category = Category(name=name)
            db.session.add(category)
        db.session.commit()
        print('Success!')
    except Exception as e:
        print(f"Error: {e}")
