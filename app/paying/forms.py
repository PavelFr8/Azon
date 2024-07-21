from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class BuyForm(FlaskForm):
    number = StringField('Номер карты', validators=[DataRequired()])
    date = StringField('Месяц/год', validators=[DataRequired()])
    cvc = StringField('CVC', validators=[DataRequired()])
    submit = SubmitField('Оплатить')