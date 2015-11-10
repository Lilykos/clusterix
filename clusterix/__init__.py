from flask import Flask

from clusterix.affiliations import models
from config import Config
from controllers.main import main


# App init
app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE
app.register_blueprint(main)


# DB init
# We have to use app context to avoid circular dependencies
models.db.init_app(app)
with app.app_context():
    models.db.create_all()
