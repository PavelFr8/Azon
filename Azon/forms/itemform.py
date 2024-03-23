from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField, IntegerField, SelectField
from wtforms.validators import DataRequired


class ItemForm(FlaskForm):
    name = StringField('Название товара', validators=[DataRequired()])
    price = IntegerField('Цена', validators=[DataRequired()])
    about = TextAreaField('О товаре', validators=[DataRequired()])
    img = FileField('Фотография товара', validators=[DataRequired()])
    category1 = SelectField('Выберите категорию товара', validators=[DataRequired()])
    category2 = SelectField('Выберите категорию товара')
    category3 = SelectField('Выберите категорию товара')
    submit = SubmitField('Сохранить', validators=[DataRequired()])