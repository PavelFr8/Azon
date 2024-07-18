from . import db_session
from data.categories import Category


def load_categories():
    categories = [
        'Без категории', 'Мужская одежда', 'Женская одежда', 'Детская одежда', 'Обувь',
        'Аксессуары', 'Электроника', 'Компьютеры и ноутбуки', 'Смартфоны и гаджеты',
        'Техника для дома', 'Мебель', 'Посуда и кухонные принадлежности',
        'Бытовая химия', 'Красота и уход', 'Спорт и фитнес', 'Книги и учебники',
        'Игрушки и игры', 'Подарки и сувениры', 'Строительство и ремонт',
        'Сад и огород', 'Для животных', 'Искусство и коллекционирование',
        'Растения и семена', 'Музыкальные инструменты', 'Фильмы и сериалы',
        'Антиквариат и винтаж', 'Еда и напитки', 'Хобби и творчество', 'Туризм и отдых',
        'Ремесла и рукоделие', 'Медицинские товары'
    ]
    sess = db_session.create_session()
    for name in categories:
        category = Category(name=name)
        sess.add(category)
    sess.commit()