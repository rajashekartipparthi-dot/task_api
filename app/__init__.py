from flask import Flask

from . import db
from .routes import bp


def create_app(config=None):
    app = Flask(__name__)
    app.config["DATABASE"] = "tasks.db"
    if config:
        app.config.update(config)

    db.init_app(app)
    app.register_blueprint(bp)
    return app
