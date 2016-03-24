from flask import Flask
from clusterix.utils.clx_logging import log_info

from .config import DATABASE
from .database import models
from .controllers.main import main


global update_msg
update_msg = ''

# App init
app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.register_blueprint(main)


# DB init
# We have to use app context to avoid circular dependencies
models.db.init_app(app)
with app.app_context():
    models.db.create_all()
