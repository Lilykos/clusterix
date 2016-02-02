from flask import Flask
from clusterix.controllers.blueprints import main

app = Flask(__name__)
app.register_blueprint(main)
