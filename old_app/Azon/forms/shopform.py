from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired


class ShopForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    about = TextAreaField('Описание')
    img = FileField('Фото', validators=[DataRequired()])
    submit = SubmitField('Зарегистрировать')
