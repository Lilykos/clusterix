from flask import Flask
from .routes import main, results


# App init
app = Flask(__name__)
app.register_blueprint(main)
app.register_blueprint(results)
