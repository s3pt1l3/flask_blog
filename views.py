from app import app
from flask import render_template
from datetime import datetime as dt


@app.route('/')
def index():
    """
    Returns index page, the main page of the Flask Blog
    """

    year = ''
    if (dt.now().year != 2021):
        year = f' - {dt.now().year}'
    return render_template('index.html', year=year)
