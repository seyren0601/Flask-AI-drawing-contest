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
        INSERT INTO user (username, group_id,salt, hashed_pw)
        VALUES (%s, %s, %s,%s)
    """
    db_cursor.execute(query,(username,group_id,salt,hashed_pw))
    mysql_client.commit()
   
    db_cursor.execute(f"SELECT * FROM user WHERE user_id = {db_cursor.lastrowid}")
    user = db_cursor.fetchall()

    return user[0]
    
def CREATE_prompt(team_id,date_time,prompt,image,submitted):
    query = """
        INSERT INTO prompts (team_id,date_time,prompt,image,submitted)
        VALUE (%s,%s,%s,%s,%s)
    """
    db_cursor.execute(query,(team_id,date_time,prompt,image,submitted))
    mysql_client.commit()

### READ ###
def GET_all_users():
    db_cursor.execute("SELECT * FROM user")
    res = db_cursor.fetchall()

    return res
    
def GET_user(user_id):
    db_cursor.execute(f"SELECT * FROM user WHERE user_id = {user_id}")
    res = db_cursor.fetchone()
    
    return res

def GET_team_prompts(team_id):
    db_cursor.execute(f"""SELECT team_id, name, prompt_id, date_time, prompt, image, submitted
                        FROM user INNER JOIN prompts ON user.user_id = prompts.team_id
                        WHERE team_id = {team_id}
                      """)
    res = db_cursor.fetchall()
    
    if len(res) == 0:
        return None
    res = date_helper.query_date_to_string(res)
    return res

def GET_prompt(prompt_id):
    db_cursor.execute(f"SELECT * FROM prompts WHERE prompt_id = {prompt_id}")
    res = db_cursor.fetchall()
    
    res = date_helper.query_date_to_string(res)
    return res

def GET_all_prompts():
    db_cursor.execute(f"SELECT * FROM prompts")
    res = db_cursor.fetchall()
    
    res = date_helper.query_date_to_string(res)
    return res