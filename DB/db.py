import mysql.connector
import os
import datetime
import json
import logging
from Helper import date_helper
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

### CREATE ###
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

def CREATE_team(team_name):
    current_date = datetime.date.today()
    sql = f'INSERT INTO team(team_name, create_date) VALUES (\"{team_name}\", \"{current_date.year}-{current_date.month}-{current_date.day}\")'
    logging.info(sql)
    db_cursor.execute(sql)
    mysql_client.commit()
    
    db_cursor.execute(f"SELECT * FROM team WHERE team_id = {db_cursor.lastrowid}")
    team = db_cursor.fetchall()
    date_helper.query_date_to_string(team)
    
    return team
    

### READ ###
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
