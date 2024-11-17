import mysql.connector
import os
import datetime
import json
import logging
import random
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
    user = date_helper.query_date_to_string(user)
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

def CREATE_assigned_submission(**kwargs):
    if len(kwargs.items()) > 0:
        submission_id = kwargs['submission_id']
        img_grader_id = kwargs['img_grader_id']
        video_grader_id = kwargs['video_grader_id']
        prompt_grader_id = kwargs['prompt_grader_id']
        query = """
            INSERT INTO assigned_submissions (submission_id, img_grader_id, video_grader_id, prompt_grader_id, status)
            VALUE (%s,%s,%s,%s,%s)
        """
        db_cursor.execute(query,(submission_id, img_grader_id, video_grader_id, prompt_grader_id, 0))

        query = f"UPDATE submission SET assigned = 1 WHERE submission_id = {submission_id}"
        db_cursor.execute(query)
        mysql_client.commit()

        db_cursor.execute(f"SELECT * FROM assigned_submissions WHERE submission_id = {submission_id}")

        assigned_submission = db_cursor.fetchall()
        date_helper.query_date_to_string(assigned_submission)
        return assigned_submission
    else:
        query = f"SELECT * FROM user WHERE group_id = 1"
        db_cursor.execute(query)
        res = db_cursor.fetchall()
        grader_list = []
        for row in res:
            grader_list.append(row['user_id'])

        query = f"SELECT * FROM submission WHERE assigned = 0"
        db_cursor.execute(query)
        submission_list = db_cursor.fetchall()

        assigned_submissions = []

        for submission in submission_list:
            print(str(submission))
            img_grader_id = grader_list[random.randint(1, len(grader_list)) - 1]
            video_grader_id = grader_list[random.randint(1, len(grader_list)) - 1]
            prompt_grader_id = grader_list[random.randint(1, len(grader_list)) - 1]
            res = CREATE_assigned_submission(submission_id=submission['submission_id'], img_grader_id=img_grader_id, video_grader_id=video_grader_id, prompt_grader_id=prompt_grader_id)
            assigned_submissions.append(res[0])

        return assigned_submissions

### READ ###
def GET_all_users():
    db_cursor.execute("SELECT * FROM user")
    res = db_cursor.fetchall()
    res = date_helper.query_date_to_string(res)
    return res
    
def GET_user(user_id):
    db_cursor.execute(f"SELECT * FROM user WHERE user_id = {user_id}")
    res = db_cursor.fetchall()
    res = date_helper.query_date_to_string(res)    
    return res

def Get_user_by_group(group_id):
    db_cursor.execute(f"SELECT * FROM user WHERE group_id = {group_id}")
    res = db_cursor.fetchall()
    res = date_helper.query_date_to_string(res)
    return res

def GET_user_authentication(username):
    db_cursor.execute(f"SELECT user_id,group_id, salt, hashed_pw FROM user WHERE username = \"{username}\"")
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
    db_cursor.execute(f"""SELECT * 
                        FROM assigned_submissions 
                        WHERE img_grader_id = {grader_id} OR video_grader_id = {grader_id} OR prompt_grader_id = {grader_id}""")
    
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
    
def UPDATE_assigned_submission(submission_id, params:dict, update_time):
    sql = f"""SELECT * FROM assigned_submissions WHERE submission_id = {submission_id}"""
    db_cursor.execute(sql)
    res = db_cursor.fetchall()
    obj_before_grade = date_helper.query_date_to_string(res)[0]
    if obj_before_grade['status']:
        raise PermissionError()


    sql = """UPDATE assigned_submissions
                            SET """
    for key,value in params.items():
        if value:
            if not obj_before_grade[key]:
                if type(value) == str:
                    sql += f" {key} = \"{value}\","
                else:
                    sql += f" {key} = {value},"
            else:
                raise ValueError()

    sql += f"modified_date = \"{update_time}\" "
    sql += f"WHERE submission_id = {submission_id}"
    db_cursor.execute(sql)
    

    sql = f"""SELECT * FROM assigned_submissions WHERE submission_id = {submission_id}"""
    db_cursor.execute(sql)
    res = db_cursor.fetchall()
    obj_after_grade = date_helper.query_date_to_string(res)[0]
    if obj_after_grade['img_score'] and obj_after_grade['video_score'] and ['prompt_score']:
        sql = f"""UPDATE assigned_submissions
                SET status = 1
                WHERE submission_id = {submission_id}"""
        db_cursor.execute(sql)
    mysql_client.commit()

### Custom query ###
def execute_select(query):
    try:
        db_cursor.execute(query)
        res = db_cursor.fetchall()        
    except Exception as e:
        return {"error": str(e)},401
    return res

def execute_insert(query):
    try:
        db_cursor.execute(query)
        mysql_client.commit()
        res = "Insert success"        
    except Exception as e:
        return {"error": str(e)},401
    return res

def execute_update(query):
    try:
        db_cursor.execute(query)
        mysql_client.commit()
        row = db_cursor.rowcount
        if row > 0:
            res = "Update success"
        else:
            res = "Update failed"        
    except Exception as e:
        return {"error": str(e)},401
    return res
###################################
