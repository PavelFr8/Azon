from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField, IntegerField, SelectField
from wtforms.validators import DataRequired

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


class ItemForm(FlaskForm):
    name = StringField('Название товара', validators=[DataRequired()])
    price = IntegerField('Цена', validators=[DataRequired()])
    about = TextAreaField('О товаре', validators=[DataRequired()])
    img = FileField('Фотография товара', validators=[DataRequired()])
    category1 = SelectField('Выберите категорию товара', validators=[DataRequired()], choices=categories,
                            render_kw={"class": "form-control", "id": "category3"})
    category2 = SelectField('Выберите категорию товара', choices=categories,
                            render_kw={"class": "form-control", "id": "category3"})
    category3 = SelectField('Выберите категорию товара', choices=categories,
                            render_kw={"class": "form-control", "id": "category3"})
    submit = SubmitField('Сохранить', validators=[DataRequired()])