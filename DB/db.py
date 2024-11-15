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
    db_cursor.execute("SELECT COUNT(*) FROM user")
    row = db_cursor.fetchone()
    if row:        
        return row['COUNT(*)']
    else:
        return 0
        
    
def CREATE_user(username,group_id,salt,hashed_pw):
    query = """
        INSERT INTO user (name, group_id,salt, hashed_pw)
        VALUES (%s, %s, %s,%s)
    """
    db_cursor.execute(query,(username,group_id,salt,hashed_pw))
    mysql_client.commit()
   
    db_cursor.execute(f"SELECT * FROM user WHERE user_id = {db_cursor.lastrowid}")
    user = db_cursor.fetchall()

    return user
    