from app import app
from flask import render_template


@app.route('/')
def index():
    """
    Returns index page, the main page of the Flask Blog
    """

    return render_template('index.html')
