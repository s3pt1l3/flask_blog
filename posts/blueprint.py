from flask import Blueprint, render_template
from models import *

posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/')
def posts_page():
    posts = select_all_posts()
    return render_template('posts.html', posts=posts)


@posts.route('/<slug>')
def post_page(slug):
    post = select_post_by_slug(slug)
    return render_template('post_page.html', post=post)
