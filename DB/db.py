import mysql.connector
import os
import datetime
import json
from Helpers import date_helper
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

def GET_user(user_id):
    db_cursor.execute(f"SELECT * FROM user WHERE user_id = {user_id}")
    res = db_cursor.fetchone()
    
    return res

def GET_all_teams():
    db_cursor.execute("SELECT * FROM team")
    res = db_cursor.fetchall()
    
    # Parse datetime value to string
    res = date_helper.query_date_to_string(res)
    
    return res

def GET_team(team_id):
    db_cursor.execute(f"SELECT * FROM team WHERE team_id = {team_id}")
    res = db_cursor.fetchall()
    
    # Parse datetime value to string
    res = date_helper.query_date_to_string(res)
    
    return res