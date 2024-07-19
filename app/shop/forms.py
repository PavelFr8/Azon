from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired


class ShopRegisterForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    about = TextAreaField('Описание')
    img = FileField('Фото', validators=[DataRequired()])
    submit = SubmitField('Зарегистрировать')


class ShopChangeInfoForm(FlaskForm):
    name = StringField('Название магазина', validators=[DataRequired()])
    about = TextAreaField('О магазине', validators=[DataRequired()])
    contact = StringField('Контактная информация', validators=[DataRequired()])
    img = FileField('Логотип магазина', validators=[DataRequired()])
    submit = SubmitField('Сохранить', validators=[DataRequired()])