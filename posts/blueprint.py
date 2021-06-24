from flask import Blueprint, render_template

posts = Blueprint('posts', __name__, template_folder='templates')

@posts.route('/')
def home():
    return render_template('posts.html')