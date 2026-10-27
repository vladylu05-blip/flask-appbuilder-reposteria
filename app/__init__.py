import logging

from flask import Flask
from flask_appbuilder import AppBuilder, Model
from flask_appbuilder.models.sqla.base import SQLA

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.INFO)

app = Flask(__name__)
app.config.from_object("config")
db = SQLA(app)

with app.app_context():
    appbuilder = AppBuilder(app, db.session)
    from . import models, views  # noqa: E402,F401
    Model.metadata.create_all(db.engine)
