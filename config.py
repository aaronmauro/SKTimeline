

DEBUG=False

#mail settings
MAIL_SERVER='smtp.gmail.com',
MAIL_PORT=465,
MAIL_USE_SSL=True,
MAIL_USERNAME = 'baaronmauro@gmail.com',
MAIL_PASSWORD = ''
# MAIL_SUPPRESS_SEND = True # put in instance/config.py for local development

# TODO: replace these
DB_HOST='localhost'
DB_USER='root'
DB_PASSWORD='pennstateerie4'
DB_NAME='sktimeline'

SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/sktimeline'

SESSION_TYPE = 'filesystem'
SECRET_KEY = 'jiboo' # change in instance config for production

#tweepy
TWEEPY_CONSUMER_KEY = 'consumer-key-here'
TWEEPY_CONSUMER_SECRET = 'consumer-secret-here'
TWEEPY_ACCESS_TOKEN_KEY = 'access-token-key-here'
TWEEPY_ACCESS_TOKEN_SECRET = 'access-token-secret-here'
