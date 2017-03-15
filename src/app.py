from flask import Flask
from .routes import main, results, projections


# App init
app = Flask(__name__)
app.register_blueprint(main)
app.register_blueprint(results)
app.register_blueprint(projections)
