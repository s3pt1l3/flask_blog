from flask import Blueprint, render_template, request, redirect, url_for
from models import *
from posts.forms import PostForm

posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/')
def posts_page():
    posts_ = select_all_posts()
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    pages = posts_.paginate(page=page, per_page=5)

    return render_template('posts.html', posts=posts_, pages=pages)


@posts.route('/<slug>')
def post_page(slug):
    post = select_post_by_slug(slug)
    return render_template('post_page.html', post=post)


@posts.route('/search')
def search():
    query = request.args.get('search')
    page = request.args.get('page')

    if query:
        posts_ = search_posts(query)
    else:
        posts_ = select_all_posts()
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    pages = posts_.paginate(page=page, per_page=5)

    return render_template('posts.html', posts=posts_, pages=pages)


@posts.route('/create', methods=['POST', 'GET'])
def new_post():
    create_form = PostForm()

    if request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text')

        post = create_post(title, text)
        return redirect(url_for('posts.post_page', slug=post.slug, post=post))

    return render_template('new_post.html', form=create_form)


@posts.route('/<slug>/edit', methods=['POST', 'GET'])
def post_update(slug):
    post = select_post_by_slug(slug)
    update_form = PostForm(obj=post)
    
    if request.method == 'POST':
        update_form = PostForm(formdata=request.form, obj=post)
        update_form.populate_obj(post)
        db.session.commit()
        return redirect(url_for('posts.post_page', slug=post.slug, post=post))
    
    return render_template('update_post.html', form=update_form, post=post)
