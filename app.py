from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Initializing Flask app
app = Flask(__name__)

# Loading app configuration
app.config.from_object(Config)

# Database
db = SQLAlchemy(app)
