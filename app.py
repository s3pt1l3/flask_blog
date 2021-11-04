from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_msearch import Search
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

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

# Admin panel
from models import *
admin = Admin(app)

admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Tag, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Role, db.session))
