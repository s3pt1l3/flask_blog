from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_msearch import Search

from config import Config

# Initializing Flask app
app = Flask(__name__)

# Loading app configuration
app.config.from_object(Config)

# Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Database search
search = Search()
search.init_app(app)
