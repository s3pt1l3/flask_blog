from flask import Blueprint, render_template, request, redirect, url_for
from models import *
from posts.forms import PostForm

posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/')
def posts_page():
    posts_ = select_all_posts()
    return render_template('posts.html', posts=posts_)


@posts.route('/<slug>')
def post_page(slug):
    post = select_post_by_slug(slug)
    return render_template('post_page.html', post=post)


@posts.route('/search')
def search():
    query = request.args.get('search')

    posts_ = search_posts(query)
    return render_template('posts.html', posts=posts_)


@posts.route('/create', methods=['POST', 'GET'])
def new_post():
    create_form = PostForm()

    if request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text')

        post = create_post(title, text)
        return redirect(url_for('posts.post_page', slug=post.slug, post=post))

    return render_template('new_post.html', form=create_form)
