from sktimeline import db
from datetime import datetime
from slackclient import SlackClient
import re
import markdown



class SlackFeedSetting(db.Model):
    __tablename__ = 'feed_setting_slack'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.uid'))
    status = db.Column( db.String(64), default=None)
    last_updated = db.Column( db.DateTime(timezone=True), default=None )

    # holds the token info, user id, team id, team name
    slack_auth_info = db.Column( db.PickleType )

    # slack machine readable id used for api request
    channel_id = db.Column( db.String(128), default=None)
    # channel info like name/description, members, etc
    channel_info = db.Column( db.PickleType )

    feed_items = db.relationship( 'SlackFeedItem' , backref='slack_feed_items', cascade="all, delete-orphan", lazy='select')

    user_data = db.Column( db.PickleType )



    _slack_client = False

    def __init__(self):
        self.status = 'new'
        self.last_updated = datetime.now()

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
        self.download_history(count=100)
        return True

    def download_history(self,count=100, oldest=0):
        self.set_updating()
        response = self.slack_client.api_call('channels.history', channel=self.channel_id, count=count, oldest=oldest)
        if response['messages']:
            for message in response['messages']:
                feed_item = SlackFeedItem()
                feed_item.timestamp = datetime.utcfromtimestamp( float(message['ts']) )
                feed_item.slack_feed_id = self.id
                feed_item.data = message
                db.session.add(feed_item)

        self.set_updated()
        db.session.commit()
        return response

    @property
    def latest_feed_item(self):
        items = SlackFeedItem.query.order_by(
                            db.desc( SlackFeedItem.timestamp  )
                        ).filter_by(
                            slack_feed_id=self.id
                        ).limit(1).all()

        if len(items) == 1:
            return items[0]
        else:
            return False

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

    def do_update(self):
        oldest = 0
        if self.latest_feed_item:
            oldest = self.latest_feed_item.ts
        self.download_history(count=1000, oldest=oldest)
        # todo: will need to see how to handle this if there are > 1000 messages to add
        return True

    @classmethod
    def update_items(cls):
        items = cls.query.filter_by(status='updated').all()
        for item in items:
            item.do_update()
        db.session.close()
        return True

    @property
    def slack_client(self):
        if not self.is_token_info_present :
            return False
        if not self._slack_client:
            self._slack_client = SlackClient(self.token)
        return self._slack_client


    @property
    def team_name(self):
        if not self.slack_auth_info:
            return False
        return self.slack_auth_info['team_name']

    @property
    def is_channel_info_present(self):
        if not self.channel_info:
            return False
        return True

    @property
    def channel_name(self):
        if not self.is_channel_info_present:
            return False
        return self.channel_info['name']

    @property
    def is_token_info_present(self):
        if not self.slack_auth_info:
            return False
        if not self.slack_auth_info['access_token']:
            return False
        return True

    @property
    def token(self):
        if not self.is_token_info_present:
            return False
        return self.slack_auth_info['access_token']


    @classmethod
    # todo: these can be dry by using module I think
    def belonging_to_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()


    def slack_user_info(self,user_id):
        if not self.user_data:
            self.user_data = {}

        if user_id in self.user_data:
            # todo: check the _time_retrieved and add and expire length time to see if we should update these records after a certain amount of time
            return self.user_data[user_id]

        user = self.slack_client.api_call('users.info', user = user_id )
        if ('ok' in user) and user['ok']:
            user = user['user']
            user['_time_retrieved'] = int( datetime.now().strftime("%s") ) #  use this time later for for determining when to update
            user_data_cache = self.user_data
            user_data_cache[user_id] = user

            self.user_data = None
            db.session.commit()

            self.user_data = user_data_cache
            db.session.commit()

            return user

        return False

    def user_name_from_id(self,user_id):
        data = self.slack_user_info(user_id)
        if not data:
            return False
        return data['name']

    def channel_name_from_id(self, channel_id):
        if channel_id == self.channel_id:
            return self.channel_name
        else:
            # for now going to make a request to the API to get the channel name here,
            # we should reconsider another approach here later where it can cache the channel info data, so that it does not continually
            # repeat the same requests over and over again
            channel_info = self.slack_client.api_call('channels.info',channel=channel_id)
            name = ''
            if channel_info['ok']:
                name = channel_info['channel']['name']
            return name




class SlackFeedItem(db.Model):
    __tablename__ = 'slack_feed_items'
    id = db.Column(db.BigInteger, primary_key=True)
    slack_feed_id = db.Column(db.Integer, db.ForeignKey('feed_setting_slack.id'))

    timestamp = db.Column( db.DateTime(timezone=True), default=None )
    data = db.Column( db.PickleType )

    @property
    def ts(self):
        return self.data['ts']



class SlackFeedItemFormatter():

    def __init__(self, slack_feed_setting, feed_item):
        self.slack_feed_setting = slack_feed_setting
        self.timestamp = feed_item.timestamp
        self.data = feed_item.data
        self._user_data = False
        self.feed_item_id = feed_item.id

    @property
    def to_json(self):
        obj = {}
        obj['type'] = 'slack'
        obj['group'] = 'Slack: ' + self.slack_feed_setting.channel_info['name']
        obj['unique_id'] = 'slack-' + self.slack_feed_setting.channel_info['name'] + '-' + str(self.feed_item_id)
        obj['text'] = {
            'headline': self.message_headline,
            'text': self.message_text
        }
        obj['start_date'] = {
          'year': self.timestamp.year,
          'month': self.timestamp.month,
          'day': self.timestamp.day,
          'hour': self.timestamp.hour,
          'minute':  self.timestamp.minute,
          'second':  self.timestamp.second
        }

        return obj

    def _replace_user_mentions(self,text):
        # this method replaces @ mention sequences of user names in the slack message text
        # ( formated like :   <@U1FSC0J67> or  <@U1FSC0J67|username> ) with the actual user name
        pattern = '(<\@(U.*?)>)'
        results = re.findall(pattern, text)
        if (len(results) > 0):
            for result in results:
                full_seq = result[0]
                user_str = full_seq.replace('<','').replace('>','')
                user_id =  user_str.split('|')[0].replace('@','')
                user_name = self.slack_feed_setting.user_name_from_id(user_id)
                text = text.replace(full_seq, '@' + user_name)
        return text

    def _replace_channel_mentions(self, text):
        # this method replaces # channel mention sequences of user names in the slack message text
        # ( formated like :  <#C1FSJK3UN> with the actual channel name
        pattern = '(<\#(C.*?)>)'
        results = re.findall(pattern, text)
        if (len(results) > 0):
            for result in results:
                full_seq = result[0]
                channel_str = full_seq.replace('<','').replace('>','')
                channel_id =  channel_str.split('|')[0].replace('#','')
                channel_name = self.slack_feed_setting.channel_name_from_id(channel_id)
                text = text.replace(full_seq, '#' + channel_name)

        return text

    @property
    def user_data(self):
        if not(self._user_data) and ('user' in self.data):
            self._user_data = self.slack_feed_setting.slack_user_info( self.data['user'] )
        return self._user_data

    @property
    def message_text(self):
        text = self.data['text']
        # escape user sequences
        text = self._replace_user_mentions(text)
        text = self._replace_channel_mentions(text)
        text = markdown.markdown(text, extensions=[SlackEmphasisToBold()])

        text = text.replace('\n','<br />')
        return text

    @property
    def message_headline(self):
        headline = False
        if not( 'subtype' in self.data ) and (self.data['type'] == 'message') and ('name' in self.user_data):
            headline = 'Message from ' + self.user_data['name']
        return headline


# replace the markdown behavior of text like *bold*... format as <strong> rather than <em>
class SlackEmphasisToBold(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        del md.inlinePatterns['emphasis']
        md.inlinePatterns['emphasis'] = markdown.inlinepatterns.SimpleTagPattern(markdown.inlinepatterns.EMPHASIS_RE, 'strong')
