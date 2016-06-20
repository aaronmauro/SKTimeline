#MySQL Database connection
import MySQLdb

def connection():
    conn = MySQLdb.connect(host="localhost", 
                          user = "root",
                          passwd = "pennstateerie4",
                          db = "sktimeline")
    c = conn.cursor()
    
    return c, conn