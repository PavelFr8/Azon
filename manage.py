from flask_migrate import Migrate
from flask_script import Manager

import os

from app import create_app, db, login_manager


app = create_app()

db.init_app(app)
with app.test_request_context():
    db.create_all()

app.config.from_object(os.environ['APP_SETTINGS'])

manager = Manager(app)
migrate = Migrate(app, db)
login_manager.init_app(app)
