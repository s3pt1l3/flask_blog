from app import app
import views
from posts.blueprint import posts
from models import *

# Bluepprints
app.register_blueprint(posts, url_prefix='/blog')

if __name__ == "__main__":
    # Creating tables in the database
    db.create_all()
    # Launching the flask application
    app.run()
