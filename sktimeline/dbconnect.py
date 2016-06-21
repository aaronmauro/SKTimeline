#MySQL Database connection
import MySQLdb
from sktimeline import app

def connection():
    conn = MySQLdb.connect(host = app.config['DB_HOST'],
                          user = app.config['DB_USER'],
                          passwd = app.config['DB_PASSWORD'],
                          db = app.config['DB_NAME'])
    c = conn.cursor()

    return c, conn
