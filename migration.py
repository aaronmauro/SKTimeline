
from flask import *
from sktimeline import *
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def setup_db():
    db.create_all()
    db.engine.execute('ALTER TABLE feed_setting_slack MODIFY user_data LONGBLOB')
    db.engine.execute('ALTER TABLE feed_setting_slack MODIFY channel_info LONGBLOB')
    db.engine.execute('ALTER TABLE github_feed_items MODIFY git_commit_data LONGBLOB')
    db.engine.execute('ALTER TABLE slack_feed_items MODIFY data LONGBLOB')
    db.engine.execute('ALTER TABLE twitter_feed_items MODIFY tweet_data LONGBLOB')
    print "Created tables"



if __name__ == '__main__':
    manager.run()
