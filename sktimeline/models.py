from sktimeline import db

class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, default=None)
    # todo: migrate to name `password`
    passwords =  db.Column(db.String(100), default=None)
    email = db.Column(db.String(50), default=None)
    settings = db.Column(db.Text, default=None)
    tracking = db.Column(db.Text, default=None)
    rank = db.Column(db.Integer, default=None)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password #todo: make it hashed
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username
