from sktimeline import db, GithubAPI
from datetime import datetime
import dateutil.parser

class GithubFeedSetting(db.Model):
    __tablename__ = 'feed_setting_github'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.uid'))

    username = db.Column( db.String(128) )
    project = db.Column( db.String(128) , default=None)
    branch = db.Column( db.String(128) , default='master')

    status = db.Column( db.String(64), default=None)
    last_updated = db.Column( db.DateTime(timezone=True), default=None )

    feed_items = db.relationship( 'GithubFeedItem' , backref='github_feed_items', cascade="all, delete-orphan", lazy='select')

    def set_updating(self):
        self.status = 'updating'
        db.session.commit()
        return self

    def set_updated(self):
        self.status = 'updated'
        self.last_updated = datetime.now()
        db.session.commit()
        return self

    def get_branch(self):
        branch = self.branch
        if ( not(self.branch) or (self.branch.strip() == '') ):
            branch = 'master'
        return branch


    @property
    def latest_feed_item(self):
        items = GithubFeedItem.query.order_by(
                            db.desc( GithubFeedItem.commit_date )
                        ).filter_by(
                            github_feed_id=self.id
                        ).limit(1).all()

        if len(items) == 1:
            return items[0]
        else:
            return False

    def download_commits(self, since=False):
        self.set_updating()
        #todo: if this feed update fails, due to exception like http error, throttle limit, etc, then
        #        we need revert the status and (probably) log the error

        if type(since) is datetime:
            commits = self.repo.get_commits(sha=self.branch, since=since )
        else:
            commits = self.repo.get_commits(sha=self.branch)

        for commit in commits:
            # when interating over this PaginatedList type of class it results in
            #  a single request downloading each commit details which may result in too many
            #  request and end up hitting our 5000 req/s rate limit -
            #    in that case may wish to use the requests lib to just make a call to api endpoint like
            #     https://api.github.com/repos/jwenerd/SKTimeline/commits?sha=github_events&per_page=100&since=2016-07-13T19:49:47Z to fetch these details in one go
            if not( self.commit_already_stored(commit.sha) ):
                feed_item = GithubFeedItem(github_feed_id=self.id, git_commit_data=commit)
                db.session.add(feed_item)

        self.set_updated()
        db.session.commit()

    def do_feed_update(self):
        since = False
        if self.latest_feed_item:
            since = self.latest_feed_item.commit_date
        self.download_commits(since=since)

    def commit_already_stored(self, sha):
        count = GithubFeedItem.query.filter_by(github_feed_id=self.id).filter_by(sha=sha).count()
        return count > 0

    @property
    def repo(self):
        repo = GithubAPI.get_repo( self.username + '/' + self.project)
        return repo

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
        for item in cls.new_items():
            item.do_feed_update()
        db.session.close()
        return True


class GithubFeedItem(db.Model):
    __tablename__ = 'github_feed_items'
    id = db.Column(db.BigInteger, primary_key=True)
    github_feed_id = db.Column(db.Integer, db.ForeignKey('feed_setting_github.id'))

    # todo: need to add an index on this due to the lookups here
    sha = db.Column( db.String(40) , default=None, index=True) # git commit id

    commit_date = db.Column( db.DateTime(timezone=True), default=None )
    date_retrieved = db.Column( db.DateTime(timezone=True), default=datetime.now )

    # throwing these all in until decide what is best to use here :/
    git_commit_data = db.Column( db.PickleType )
    #  other potential ideas: github_commit data -   includes stuff like author data


    def __init__(self, github_feed_id=github_feed_id, git_commit_data=git_commit_data ):

        self.github_feed_id = github_feed_id
        self.date_retrieved = datetime.now()
        self.sha = git_commit_data.sha
        self.git_commit_data = git_commit_data.raw_data['commit']
        self.commit_date = dateutil.parser.parse( git_commit_data.raw_data['commit']['committer']['date'] ).replace( tzinfo=None )
        # todo: replace time may be wrong for time zones - we need a way how to treat this :/

    @property
    def to_json(self):
        obj = {}
        obj['data'] = self.git_commit_data
        obj['text'] = {
            'headline': 'Commit',
            'text': '<p>' +  self.git_commit_data['message'] + '<br><br>by ' + self.git_commit_data['committer']['name'] + ' &lt;' +self.git_commit_data['committer']['name'] + '&gt;</p>' 
            # todo: above is a basic example of using html templatea in a timeilne text node,
            #           will want to see what data we want, and for ease of use use a jinja template or _.js template to make formatting this easier
        }
        obj['start_date'] = {
          'year': self.commit_date.year,
          'month': self.commit_date.month,
          'day': self.commit_date.day,
          'hour': self.commit_date.hour,
          'minute':  self.commit_date.minute,
          'second':  self.commit_date.second
        }

        return obj;
