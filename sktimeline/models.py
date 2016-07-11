from sktimeline import db
from passlib.hash import sha256_crypt
from datetime import datetime
from sktimeline import tweepy, tweepy_API


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
    slack_feed_settings = db.relationship('SlackFeedSetting', backref='user', lazy='select')
    github_feed_settings =  db.relationship('GithubFeedSetting', backref='user', lazy='select')

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
    # handle = db.Column( db.String(64) )
    hashtag = db.Column( db.String(128), default=None)
    status = db.Column( db.String(64), default=None)
    last_updated = db.Column( db.DateTime(timezone=True), default=None )

    feed_items = db.relationship( 'TwitterFeedItem' , backref='feed_setting_twitter', cascade="all, delete-orphan", lazy='select')

    #todo: move method that starts adding hashtags here

    def set_updating(self):
        self.status = 'updating'
        db.session.commit()
        return self

    def set_updated(self):
        self.status = 'updated'
        self.last_updated = datetime.now()
        db.session.commit()
        return self

    def start_populate(self):
        # download 200 latest tweets with this hash tag, this can go up to 1500 according to twitter api docs
        self.download_tweets(max_tweets=200)
        return True

    def get_last_tweet_id_downloaded(self):
        return db.session.query(db.func.max( TwitterFeedItem.tweet_id) ).filter_by(twitter_feed_id=self.id).scalar()

    def download_tweets(self, since_id=False, max_tweets=100):

        query = self.hashtag
        self.set_updating()
        if since_id:
            hashtag_tweets = [status for status in tweepy.Cursor(tweepy_API.search, rpp=100, q=query, since_id=since_id).items(max_tweets)]
        else:
            hashtag_tweets = [status for status in tweepy.Cursor(tweepy_API.search, rpp=100, q=query).items(max_tweets)]

        for tweet in hashtag_tweets:
            feed_item = TwitterFeedItem(tweet.id, self.id, tweet)
            db.session.add(feed_item)
        self.set_updated()
        db.session.commit()


    def do_feed_update(self):
        last_tweet = self.get_last_tweet_id_downloaded()
        if ( not(last_tweet) ):
            self.start_populate()
        else:
            self.download_tweets(since_id=last_tweet)
        return True

    @classmethod
    def belonging_to_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def update_items(cls):
        items = cls.query.filter_by(status='updated').all()
        for item in items:
            item.do_feed_update()
        db.session.close()
        return True


    @classmethod
    def new_items(cls):
        return cls.query.filter_by(status='new').all()

    @classmethod
    def start_populate_new_items(cls):
        new_items = cls.new_items()
        for item in new_items:
            item.start_populate()
        db.session.close()
        return True

class SlackFeedSetting(db.Model):
    __tablename__ = 'feed_setting_slack'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.uid'))
    team = db.Column( db.String(256), default=None )
    channel = db.Column( db.String(256), default=None)

    @classmethod
    # todo: these can be dry by using module I think
    def belonging_to_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

class GithubFeedSetting(db.Model):
    __tablename__ = 'feed_setting_github'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.uid'))
    username = db.Column( db.String(64) )
    project = db.Column( db.String(64) , default=None)

    @classmethod
    def belonging_to_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

class TwitterFeedItem(db.Model):
    __tablename__ = 'twitter_feed_items'
    id = db.Column(db.BigInteger, primary_key=True)
    twitter_feed_id = db.Column(db.Integer, db.ForeignKey('feed_setting_twitter.id'))
    tweet_id = db.Column( db.BigInteger )
    tweet_retrieved = db.Column( db.DateTime(timezone=True), server_default=db.func.now() )
    tweet_data = db.Column( db.PickleType )

    def __init__(self, tweet_id, twitter_feed_id, tweet_data):
        self.tweet_id = tweet_id
        self.twitter_feed_id = twitter_feed_id
        self.tweet_data = tweet_data

    def status_url(self):
        return ( 'https://twitter.com/statuses/' + str(self.tweet_id) )

    def as_timelinejs_event(self):
        obj = {}
        obj['media'] = {
            'url': self.status_url()
        }
        obj['start_date'] = {
          'year': self.tweet_data.created_at.year,
          'month': self.tweet_data.created_at.month,
          'day': self.tweet_data.created_at.day,
          'hour': self.tweet_data.created_at.hour,
          'minute':  self.tweet_data.created_at.minute,
          'second':  self.tweet_data.created_at.second
        }

        return obj;
