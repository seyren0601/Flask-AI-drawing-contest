import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

db_user = os.environ["DB_USER"]
db_password = os.environ["DB_PASSWORD"]
mysql_client = mysql.connector.connect(
    host="localhost",
    user=db_user,
    password=db_password,
    database="ai_drawing_contest"
)

db_cursor = mysql_client.cursor(dictionary=True)

def GET_all_users():
    db_cursor.execute("SELECT * FROM user")
    res = db_cursor.fetchall()

    return res


def Count_user():
    db_cursor.execute("SELECT COUNT(*) FROM users")
    row = db_cursor.fetchone()[0]
    return row
    
def CREATE_user(username,salt,hashedpw):
    query = """
        INSERT INTO users (username, salt, hashed_password)
        VALUES (%s, %s, %s)
    """
    db_cursor.execute(query,(username,salt,hashedpw))
    mysql_client.commit()
    