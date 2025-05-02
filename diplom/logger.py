import pymysql

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "12345678"
DB_NAME = "distillery_db"

def log_action(username, action):
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO activity_log (username, action) VALUES (%s, %s)", (username, action))
    conn.commit()
    conn.close()
