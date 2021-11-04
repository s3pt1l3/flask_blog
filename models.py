from datetime import datetime
import re

from flask_security import UserMixin, RoleMixin

from app import db

"""PostsTags tabel model (many to many relationship for posts and tags)"""
posts_tags = db.Table('PostsTags', db.Column('post_id', db.Integer, db.ForeignKey(
    'Posts.post_id')), db.Column('tag_id', db.Integer, db.ForeignKey('Tags.tag_id')))


"""UsersRoles tabel model (many to many relationship for users and roles)"""
users_roles = db.Table('UsersRoles', 
                       db.Column('user_id', db.Integer, db.ForeignKey('Users.user_id')), 
                       db.Column('role_id', db.Integer, db.ForeignKey('Roles.role_id')))


class Post(db.Model):
    """
    Posts tabel model

    `post_id`: Post id
    `title`: Post title
    `slug`: Post slug
    `text`: Post text
    `tags`: Tags relationship
    `created_at`: When the post was created
    """

    __tablename__ = "Posts"
    __searchable__ = ['title', 'text', 'tags']

    post_id = db.Column(db.Integer,  primary_key=True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)
    text = db.Column(db.Text)
    tags = db.relationship('Tag', secondary=posts_tags,
                           backref=db.backref('Posts'), lazy='dynamic')
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__generate_slug()

    def __repr__(self) -> str:
        return f'Post id: {self.post_id}\nPost title: {self.title}\nCreated at: {self.created_at}'

    def __generate_slug(self) -> None:
        """
        Creating post slug from post title 
        """

        if self.title:
            self.slug = self.__slugify(self.title)
        else:
            self.slug = str(datetime.now())

    def __slugify(self, s: str) -> str:
        """
        Generates slug string
        """

        return re.sub(r'[^\w+]', '-', s).lower()


"""Posts functions"""


def create_post(title: str, text: str) -> Post:
    """
    Function that creates post record in database and returns Post instance

    `title`: Post title
    `text`: Post text
    """

    post = Post(title=title, text=text)
    db.session.add(post)
    db.session.commit()

    return post


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

    return Post.query


def delete_post(post_id: int):
    """
    Function that deletes post record

    `post_id`: Post id
    """

    Post.query.filter(Post.post_id == post_id).first().delete()
    db.session.commit()


def search_posts(query: str):
    """
    Function for searching post by query (post title and post text search)

    `query`: Search query
    """

    return Post.query.filter(Post.title.contains(query) | Post.text.contains(query))


class Tag(db.Model):
    """
    Tags tabel model

    `tag_id`: Tag id
    `title`: Tag title
    `slug`: Tag slug
    `created_at`: When the tag was created
    """

    __tablename__ = "Tags"

    tag_id = db.Column(db.Integer,  primary_key=True)
    title = db.Column(db.String(100))
    slug = db.Column(db.String(140), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__generate_slug()

    def __repr__(self) -> str:
        return f'Tag id: {self.tag_id}\nTag title: {self.title}\nCreated at: {self.created_at}'

    def __generate_slug(self) -> None:
        """
        Creating post slug from post title 
        """

        if self.title:
            self.slug = self.__slugify(self.title)
        else:
            self.slug = str(datetime.now())

    def __slugify(s: str) -> str:
        """
        Generates slug string
        """

        return re.sub(r'[^\w+]', '-', s).lower()


"""Tags functions"""


def create_tag(title: str):
    """
    Function that creates tag record in database

    `title`: Tag title
    """

    tag = Tag(title=title)
    db.session.add(tag)
    db.session.commit()


def select_tag(tag_id: int):
    """
    Function that gets tag record from database

    `tag_id`: Tag id
    """

    return Tag.query.filter(Post.tag_id == tag_id).first()


def select_all_tags():
    """
    Function that gets all tags records from database
    """

    return Tag.query.all()


def delete_tag(tag_id: int):
    """
    Function that deletes tag record

    `tag_id`: Tag id
    """

    Post.query.filter(Tag.tag_id == tag_id).first().delete()
    db.session.commit()


class User(db.Model, UserMixin):
    """
    Users tabel model

    `user_id`: User id
    `email`: User email
    `password`: User password
    `roles`: Roles relationship
    `created_at`: When the user was created
    """
    
    __tablename__ = "Users"
    
    user_id = db.Column(db.Integer,  primary_key=True)
    email = db.Column(db.String(320), unique=True)
    password = db.Column(db.String(255))
    roles = db.relationship('Role', secondary=users_roles, backref=db.backref('Users'), lazy='dynamic')
    created_at = db.Column(db.DateTime, default=datetime.now())


class Role(db.Model, RoleMixin):
    """
    Roles tabel model

    `role_id`: Role id
    `name`: Role name
    `created_at`: When the role was created
    """
    
    __tablename__ = "Roles"
    
    role_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    