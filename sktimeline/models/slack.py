from sktimeline import db


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
