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
def CREATE_user(username,group_id,salt,hashed_pw,date_string):
    query = """
        INSERT INTO user (username, group_id,salt, hashed_pw, register_date)
        VALUES (%s, %s, %s,%s, %s)
    """
    db_cursor.execute(query,(username,group_id,salt,hashed_pw,date_string))
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

def CREATE_submission(prompt_id,submit_date,video,score):
    query = """
        INSERT INTO submission (prompt_id,submit_date,video,score)
        VALUE (%s,%s,%s,%s)
    """
    db_cursor.execute(query,(prompt_id,submit_date,video,score))
    mysql_client.commit()

    db_cursor.execute(f"SELECT * FROM submission WHERE submission_id = {db_cursor.lastrowid}")
    submission = db_cursor.fetchall()
    date_helper.query_date_to_string(submission)
    return submission

def CREATE_assigned_submission(submission_id, img_grader_id, video_grader_id, prompt_grader_id):
    query = """
        INSERT INTO assigned_submissions (submission_id, img_grader_id, video_grader_id, prompt_grader_id, status)
        VALUE (%s,%s,%s,%s,%s)
    """
    db_cursor.execute(query,(submission_id, img_grader_id, video_grader_id, prompt_grader_id, 0))
    mysql_client.commit()

    db_cursor.execute(f"SELECT * FROM assigned_submissions WHERE submission_id = {submission_id}")

    assigned_submission = db_cursor.fetchall()
    date_helper.query_date_to_string(assigned_submission)
    return assigned_submission

### READ ###
def GET_all_users():
    db_cursor.execute("SELECT * FROM user")
    res = db_cursor.fetchall()
    return res
    
def GET_user(user_id):
    db_cursor.execute(f"SELECT * FROM user WHERE user_id = {user_id}")
    res = db_cursor.fetchall()
    res = date_helper.query_date_to_string(res)    
    return res

def GET_user_authentication(username):
    db_cursor.execute(f"SELECT user_id, salt, hashed_pw FROM user WHERE username = \"{username}\"")
    res = db_cursor.fetchall()
    
    return res

def GET_team_prompts(team_id):
    db_cursor.execute(f"""SELECT team_id, name, prompt_id, date_time, prompt, image, submitted
                        FROM user INNER JOIN prompts ON user.user_id = prompts.team_id
                        WHERE team_id = {team_id}
                      """)
    res = db_cursor.fetchall()
    
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

def GET_all_submissions():
    db_cursor.execute(f"SELECT * FROM submission")
    res = db_cursor.fetchall()
    
    res = date_helper.query_date_to_string(res)
    return res

def GET_submission(submission_id):
    db_cursor.execute(f"SELECT * FROM submission WHERE submission_id = {submission_id}")
    res = db_cursor.fetchall()
    
    res = date_helper.query_date_to_string(res)
    return res

def GET_team_submission(team_id):
    db_cursor.execute(f"""SELECT submission_id, submission.prompt_id, submit_date, video, score
                            FROM submission INNER JOIN prompts ON prompts.prompt_id = submission.prompt_id
                            WHERE prompts.team_id = {team_id}""")
    res = db_cursor.fetchall()
    
    res = date_helper.query_date_to_string(res)
    return res

def GET_grader_assigned_submissions(grader_id):
    db_cursor.execute(f"SELECT * FROM assigned_submissions WHERE grader_id = {grader_id}")
    
    res = db_cursor.fetchall()
    
    res = date_helper.query_date_to_string(res)
    return res

def GET_assigner_assigned_submissions(assigner_id):
    db_cursor.execute(f"SELECT * FROM assigned_submissions WHERE assinger_id = {assigner_id}")
    
    res = db_cursor.fetchall()
    
    res = date_helper.query_date_to_string(res)
    return res

def GET_assigned_submission(submission_id):
    db_cursor.execute(f"SELECT * FROM assigned_submissions WHERE submission_id = {submission_id}")
    
    res = db_cursor.fetchall()
    
    res = date_helper.query_date_to_string(res)
    return res

def GET_all_assigned_submissions():
    db_cursor.execute(f"SELECT * FROM assigned_submissions")
    
    res = db_cursor.fetchall()
    
    res = date_helper.query_date_to_string(res)
    return res 
    
### Update ###
def UPDATE_user(user_id, update_data):
    params = []
    updates = []
    for key , value in update_data.items():
        if value is not None:
            updates.append(f"{key} = %s")
            params.append(value)

    params.append(user_id)
    
    query = f"""UPDATE user 
                SET {', '.join(updates)}
                WHERE user_id = %s"""
    db_cursor.execute(query,tuple(params))
    mysql_client.commit()
    print("User updated successfully.")

def UPDATE_prompt(prompt_id):
    db_cursor.execute(f"UPDATE prompts SET submitted = 1 WHERE prompt_id = {prompt_id}")
    mysql_client.commit()
    
def UPDATE_assigned_submission(submission_id, status, comment, score, update_time):
    db_cursor.execute(f"""UPDATE assigned_submissions
                            SET status = {status}, comment = \"{comment}\", modified_date = \"{update_time}\"
                            WHERE submission_id = {submission_id}""")
    
    db_cursor.execute(f"""UPDATE submission
                            SET score = {score}
                            WHERE submission_id = {submission_id}""")
    mysql_client.commit()

