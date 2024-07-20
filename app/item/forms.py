from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField, IntegerField, SelectField
from wtforms.validators import DataRequired

from app.utils.load_categories import categories


class CommentForm(FlaskForm):
    text = TextAreaField('Комментарий', validators=[DataRequired()])
    submit = SubmitField('Вход')


class ItemForm(FlaskForm):
    name = StringField('Название товара', validators=[DataRequired()])
    price = IntegerField('Цена', validators=[DataRequired()])
    about = TextAreaField('О товаре', validators=[DataRequired()])
    img = FileField('Фотография товара')
    category1 = SelectField('Выберите категорию товара', validators=[DataRequired()], choices=categories,
                            render_kw={"class": "form-control", "id": "category3"})
    category2 = SelectField('Выберите категорию товара', choices=categories,
                            render_kw={"class": "form-control", "id": "category3"})
    category3 = SelectField('Выберите категорию товара', choices=categories,
                            render_kw={"class": "form-control", "id": "category3"})
    submit = SubmitField('Сохранить', validators=[DataRequired()])