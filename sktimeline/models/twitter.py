from sktimeline import db
from sktimeline import tweepy, tweepy_API
from datetime import datetime
import re

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





class TwitterFeedItem(db.Model):
    __tablename__ = 'twitter_feed_items'
    id = db.Column(db.BigInteger, primary_key=True)
    twitter_feed_id = db.Column(db.Integer, db.ForeignKey('feed_setting_twitter.id'))
    tweet_id = db.Column( db.BigInteger )
    tweet_retrieved = db.Column( db.DateTime(timezone=True), default=datetime.now )
    tweet_data = db.Column( db.PickleType )

    def __init__(self, tweet_id, twitter_feed_id, tweet_data):
        self.tweet_id = tweet_id
        self.twitter_feed_id = twitter_feed_id
        self.tweet_data = tweet_data

    @property
    def status_url(self):
        return ( 'https://twitter.com/statuses/' + str(self.tweet_id) )







class TwitterFeedItemFormatter:
    def __init__(self, twitter_feed_setting, feed_item):
        self.twitter_feed_setting = twitter_feed_setting
        self.feed_item = feed_item
        self.timestamp = self.feed_item.tweet_data.created_at
        self._photo_media_url = None

    def photo_media_url(self):
        if self._photo_media_url is not None:
            return self._photo_media_url

        self._photo_media_url = False
        if not 'media' in self.feed_item.tweet_data.entities:
            return False

        for e in self.feed_item.tweet_data.entities['media']:
            if 'type' in e and e['type'] == 'photo':
                self._photo_media_url = e['media_url']
                break
        return self._photo_media_url


    @property
    def unique_id(self):
        hashtag_attr = self.twitter_feed_setting.hashtag.strip()
        #hashtag as attribute - remove spaces and non alpha numeric chars
        hashtag_attr = re.sub(r"[^\w\s]", '', hashtag_attr)
        # Replace all runs of whitespace with a single dash
        hashtag_attr = re.sub(r"\s+", '-', hashtag_attr)

        return 'tweet-' + hashtag_attr + '-' + str(self.feed_item.tweet_id)

    @property
    def to_json(self):
        obj = {}
        obj['type'] = 'twitter'
        obj['tweet_text'] = self.feed_item.tweet_data.text
        obj['group'] = 'Twitter: ' + self.twitter_feed_setting.hashtag
        obj['unique_id'] = self.unique_id
        obj['media'] = {
            'url': self.feed_item.status_url
            # todo: add thumbnail here
        }
        media_url = self.photo_media_url()
        if media_url:
            obj['background'] = { 'url': media_url }
        obj['start_date'] = {
          'year': self.timestamp.year,
          'month': self.timestamp.month,
          'day': self.timestamp.day,
          'hour': self.timestamp.hour,
          'minute':  self.timestamp.minute,
          'second':  self.timestamp.second
        }
        return obj
