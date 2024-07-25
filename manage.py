from flask import request
from flask_login import login_user
from flask_migrate import Migrate

import click

from app import create_app, db, login_manager
from app.utils.inject import inject
from app.utils.load_categories import load_categories
from app.models import User


app = create_app()

db.init_app(app)
with app.test_request_context():
    db.create_all()

# Command for loading items categories to database
@click.command(name="category_load")
def category_load():
    load_categories()

app.cli.add_command(category_load)
migrate = Migrate(app, db)
login_manager.init_app(app)
app.context_processor(inject)

# настройка передачи залогиненных пользователей
@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    return user