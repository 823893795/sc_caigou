from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .views import bp
from .utils import scheduler

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.BaseConfig")
    db.init_app(app)

    app.register_blueprint(bp)

    scheduler.init_app(app)
    scheduler.start()

    return app

