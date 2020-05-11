from flask_migrate import Migrate
from .postgresql import db

def init_app(app):
    db.init_app(app)
    migrate = Migrate(app, db)