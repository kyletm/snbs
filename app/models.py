from datetime import datetime
from hashlib import md5
from time import time
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import app, db, login
from sqlalchemy.orm import class_mapper

followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

def attribute_names(cls):
    return [prop.key for prop in class_mapper(cls).iterate_properties
        if isinstance(prop, sqlalchemy.orm.ColumnProperty)]

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    institution = db.Column(db.String(120))
    posts = db.relationship('Post', backref='author', lazy='dynamic', primaryjoin='foreign(Post.user_id) == user.c.id')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0
    
    def can_be_reviewed_by(self, user):
        return self.posts.filter(db.and_(Post.purchaser == user, Post.expired == False)).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    demand = db.Column(db.String(3))
    broad_category = db.Column(db.String(8))
    category = db.Column(db.String(20))
    price = db.Column(db.Numeric)
    title = db.Column(db.String(140))
    body = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    institution = db.Column(db.String(140))
    purchased = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', foreign_keys=[user_id], backref='user')
    purchased_id = db.Column(db.Integer, db.ForeignKey('user.id', use_alter=True, name='fk_purchased_user_id'), default=None)
    purchaser = db.relationship('User', foreign_keys=[purchased_id], post_update=True)
    expired = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Post {}>'.format(self.body)
    
    def add_purchaser(self, user):
        if self.purchased == False:
            self.purchaser_id = user.id
            self.purchaser = user
            self.purchased = True

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reviewer = db.relationship('User', foreign_keys=[reviewer_id])
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    reviewee_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reviewee = db.relationship('User', foreign_keys=[reviewee_id])
    rating = db.Column(db.String(120))
    body = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Review {}>'.format(self.body)
