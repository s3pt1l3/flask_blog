from flask import Flask
from flask.helpers import url_for
from config import Config
from posts.blueprint import posts


app = Flask(__name__)
app.config.from_object(Config)

# Bluepprints
app.register_blueprint(posts, url_prefix='/blog')
