from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Вход')


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired(), Email(message=None), Length(min=6, max=40)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6, max=40)])
    password_again = PasswordField('Повторить пароль', validators=[DataRequired(), EqualTo("password", message="Пароли не совпадают!")])
    submit = SubmitField('Зарегистрироваться')
