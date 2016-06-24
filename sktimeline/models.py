from sktimeline import db
from passlib.hash import sha256_crypt

class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True) #todo: maybe write migration to rename to id to be consistant
    username = db.Column(db.String(20), unique=True, default=None)
    # todo: write migration to name `password`
    passwords =  db.Column(db.String(100), default=None)
    email = db.Column(db.String(50), default=None)
    settings = db.Column(db.Text, default=None)
    tracking = db.Column(db.Text, default=None)
    rank = db.Column(db.Integer, default=None)

    twitter_feed_settings = db.relationship('TwitterFeedSetting', backref='user', lazy='select')

    def __init__(self, username, password, email):
        self.username = username
        self.passwords = sha256_crypt.encrypt(password)
        self.email = email

    def password_is_correct(self, password):
        return sha256_crypt.verify(password, self.passwords)

    @classmethod
    def username_exists(cls, username):
        # todo: look if this query.filter method is proper way to query
        return cls.query.filter(cls.username == username).count() > 0

    @classmethod
    def load_by_username(cls, username):
        return cls.query.filter_by(username=username).first()


    def __repr__(self):
        return '<User %r>' % self.username


class TwitterFeedSetting(db.Model):
    __tablename__ = 'feed_setting_twitter'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.uid'))
    handle = db.Column( db.String(64) )
    hashtags = db.Column(db.Text, default=None)

    @classmethod
    def belonging_to_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()
