from flask_migrate import Migrate
from flask_script import Manager
import click

from app import create_app, db, login_manager
from app.utils.inject import inject
from app.utils.load_categories import load_categories


app = create_app()

db.init_app(app)
with app.test_request_context():
    db.create_all()

# Command for loading items categories to database
@click.command(name="category_load")
def category_load():
    load_categories()

app.cli.add_command(category_load)
manager = Manager(app)
migrate = Migrate(app, db)
login_manager.init_app(app)
app.context_processor(inject)



