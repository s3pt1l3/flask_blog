from datetime import datetime
import re
from app import db


class Post(db.Model):
    """
    Posts tabel model

    `post_id`: Post id
    `title`: Post title
    `slug`: Post slug
    `text`: Post text
    `created_at`: When the post was created
    """

    post_id = db.Column(db.Integer,  primary_key=True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)
    text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return f'Post id: {self.post_id}\nPost title: {self.title}\nCreated at: {self.created_at}'

    def __generate_slug(self) -> None:
        """
        Creating post slug from post title 
        """

        if self.title:
            self.slug = self.slugify(self.title)
        else:
            self.slug = str(datetime.now())

    def __slugify(s: str) -> str:
        """
        Generates slug string
        """

        return re.sub(r'[^\w+]', '-', s).lower()


def create_post(title: str, text: str):
    """
    Function that creates post record in database

    `title`: Post title
    `text`: Post text
    """

    post = Post(title=title, text=text)
    db.session.add(post)
    db.session.commit()


def select_post(post_id: int):
    """
    Function that gets post record from database

    `post_id`: Post id
    """

    return Post.query.filter(Post.post_id == post_id).first()


def select_post_by_slug(slug: str):
    """
    Function that gets post record from database by slug

    `slug`: Post slug
    """

    return Post.query.filter(Post.slug == slug).first()


def select_all_posts():
    """
    Function that gets all posts records from database
    """

    return Post.query.all()


def update_post(post_id: int, title: str = None, text: str = None):
    """
    Function that updates post record from database

    `post_id`: Post id
    `title`: New post title
    `text`: New post text
    """

    if title is not None:
        Post.query.filter(Post.post_id == post_id).first().update(
            {'title': title})
    if text is not None:
        Post.query.filter(Post.post_id == post_id).first().update(
            {'text': text})
    db.session.commit()


def delete_post(post_id: int):
    """
    Function that deletes post record

    `post_id`: Post id
    """

    Post.query.filter(Post.post_id == post_id).first().delete()
    db.session.commit()
