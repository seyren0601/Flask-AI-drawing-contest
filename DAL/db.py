import mysql.connector
import os
import datetime
import json
import logging
import random
from Helper import date_helper
from dotenv import load_dotenv
from Models.user import User
from Models.prompt import Prompt
from flask_sa import db
import sqlalchemy.sql

load_dotenv()

db_user = os.environ["DB_USER"]
db_password = os.environ["DB_PASSWORD"]
def init_connection():
    mysql_client = mysql.connector.connect(
        host="localhost",
        user=db_user,
        password=db_password,
        database="ai_drawing_contest"
    )    
    return mysql_client

def init_cursor(client):
    db_cursor = client.cursor(dictionary=True)

    return db_cursor

### CREATE ###
def CREATE_user(insert_data):   
    if len(insert_data.items()) == 4:
        new_User = User(
        group_id = insert_data["group_id"],
        salt = insert_data["salt"],
        hashed_pw = insert_data["hashed_pw"],
        register_date = insert_data["register_date"]        
    )
    else:
        new_User = User(
            group_id = insert_data["group_id"],
            salt = insert_data["salt"],
            hashed_pw = insert_data["hashed_pw"],
            register_date = insert_data["register_date"],
            name = insert_data["name"],
            email = insert_data["email"],
            phone_number = insert_data["phone_number"],
            school_name =  insert_data["school_name"],
            grade =  insert_data["grade"],       
            team_info = insert_data["team_info"]
        )
    db.session.add(new_User)
    db.session.commit()
    # Create user name
    user_id = new_User.user_id
    username = "usr" + str(user_id).zfill(5)
    new_User.username = username
    db.session.commit()
    # Return user
    user = db.session.scalars(
        sqlalchemy.select((User))
        .where(User.user_id == new_User.user_id)
    ).one()
    return user.toJSON()

def CREATE_user_manually(insert_data):
    new_User = User(
        group_id = insert_data["group_id"],
        salt = insert_data["salt"],
        hashed_pw = insert_data["hashed_pw"],
        register_date = insert_data["register_date"],
        name = insert_data["name"],
        email = insert_data["email"],
        phone_number = insert_data["phone_number"],
        school_name =  insert_data["school_name"],
        grade =  insert_data["grade"],       
        team_info = insert_data["team_info"],                        
    )   
    db.session.add(new_User)
    db.session.commit()
    # Create user name
    user_id = new_User.user_id
    username = "usr" + str(user_id).zfill(5)
    new_User.username = username
    db.session.commit() 
    # Return user
    user = db.session.scalars(
        sqlalchemy.select((User))
        .where(User.user_id == new_User.user_id)
    ).one()
    return user.toJSON()

def CREATE_prompt(team_id,date_time,prompt,image):
    with init_connection() as mysql_client:
        db_cursor = init_cursor(mysql_client)
                
        query = """
            INSERT INTO prompts (team_id,date_time,prompt,image,submitted)
            VALUE (%s,%s,%s,%s, 0)
        """
        db_cursor.execute(query,(team_id,date_time,prompt,image))
        mysql_client.commit()

def CREATE_submission(prompt_id,submit_date):
    with init_connection() as mysql_client:
        db_cursor = init_cursor(mysql_client)
        
        query = f"""WITH q AS(
                        SELECT team_id
                        FROM prompts
                        WHERE prompts.prompt_id = {prompt_id}
                    )
                    SELECT *
                    FROM prompts
                    WHERE team_id = (SELECT * FROM q) AND submitted=1
                    """
        db_cursor.execute(query)
        res = db_cursor.fetchall()
        if len(res) > 0:
            team_id = res[0]['team_id']
            raise PermissionError("Submission limit exceeded")
        
        query = """
            INSERT INTO submission (prompt_id,submit_date,assigned)
            VALUE (%s,%s, 0)
        """
        db_cursor.execute(query,(prompt_id,submit_date))
        mysql_client.commit()

        db_cursor.execute(f"SELECT * FROM submission WHERE submission_id = {db_cursor.lastrowid}")
        submission = db_cursor.fetchall()
        date_helper.query_date_to_string(submission)
        return submission[0]

def CREATE_assigned_submission(**kwargs):
    with init_connection() as mysql_client:
        db_cursor = init_cursor(mysql_client)
        if len(kwargs.items()) > 0:
            submission_id = kwargs['submission_id']
            img_grader_id = kwargs['img_grader_id']            
            prompt_grader_id = kwargs['prompt_grader_id']
            query = """
                INSERT INTO assigned_submissions (submission_id, img_grader_id,prompt_grader_id, status)
                VALUE (%s,%s,%s,%s)
            """
            db_cursor.execute(query,(submission_id, img_grader_id, prompt_grader_id, 0))

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
                prompt_grader_id = grader_list[random.randint(1, len(grader_list)) - 1]
                res = CREATE_assigned_submission(submission_id=submission['submission_id'], img_grader_id=img_grader_id, prompt_grader_id=prompt_grader_id)
                assigned_submissions.append(res[0])

            return assigned_submissions

### READ ###
def GET_all_users():
    # with init_connection() as mysql_client:
    #     db_cursor = init_cursor(mysql_client)
    #     db_cursor.execute("SELECT * FROM user")
    #     res = db_cursor.fetchall()
    #     res = date_helper.query_date_to_string(res)
    #     return res
    
    users = db.session.query(User)
    return [user.toJSON() for user in users]
    
def GET_user(user_id):
    with init_connection() as mysql_client:
        db_cursor = init_cursor(mysql_client)
        db_cursor.execute(f"SELECT * FROM user WHERE user_id = {user_id}")
        res = db_cursor.fetchall()
        res = date_helper.query_date_to_string(res)
        if len(res) == 0:
            raise ValueError()
        return res[0]

def Get_user_by_group(group_id):
    with init_connection() as mysql_client:
        db_cursor = init_cursor(mysql_client)
        db_cursor.execute(f"SELECT * FROM user WHERE group_id = {group_id}")
        res = db_cursor.fetchall()
        res = date_helper.query_date_to_string(res)
        return res

def GET_user_authentication(username):
    with init_connection() as mysql_client:
        db_cursor = init_cursor(mysql_client)
        db_cursor.execute(f"SELECT user_id,group_id, salt, hashed_pw FROM user WHERE username = \"{username}\"")
        res = db_cursor.fetchall()
        
        return res

def GET_team_prompts(team_id):
    # with init_connection() as mysql_client:
    #     db_cursor = init_cursor(mysql_client)
    #     db_cursor.execute(f"""SELECT team_id, name, prompt_id, date_time, prompt, image, submitted
    #                         FROM user INNER JOIN prompts ON user.user_id = prompts.team_id
    #                         WHERE team_id = {team_id}
    #                     """)
    #     res = db_cursor.fetchall()
        
    #     res = date_helper.query_date_to_string(res)
    #     return res
    
    prompts = db.session.scalars(
        sqlalchemy.select((Prompt))
        .where(Prompt.team_id == team_id)
    ).all()
    
    return [prompt.toJson() for prompt in prompts]

def GET_prompt(prompt_id):
    with init_connection() as mysql_client:
        db_cursor = init_cursor(mysql_client)
        db_cursor.execute(f"SELECT * FROM prompts WHERE prompt_id = {prompt_id}")
        res = db_cursor.fetchall()
        
        res = date_helper.query_date_to_string(res)
        return res

def GET_all_prompts():
    # with init_connection() as mysql_client:
    #     db_cursor = init_cursor(mysql_client)
    #     db_cursor.execute(f"SELECT * FROM prompts")
    #     res = db_cursor.fetchall()
        
    #     res = date_helper.query_date_to_string(res)
    #     return res
        
        prompts = db.session.query(Prompt)
        return [prompt.toJson() for prompt in prompts]

def GET_all_submissions():
    with init_connection() as mysql_client:
        db_cursor = init_cursor(mysql_client)

        sql = f"""SELECT name as team_name, submission_id, submission.prompt_id, submit_date, assigned
                    FROM submission 
                        INNER JOIN prompts ON submission.prompt_id = prompts.prompt_id
                        INNER JOIN user ON user.user_id = prompts.team_id
                """

        db_cursor.execute(sql)
        res = db_cursor.fetchall()
        
        res = date_helper.query_date_to_string(res)
        return res

def GET_submission(submission_id):
    with init_connection() as mysql_client:
        db_cursor = init_cursor(mysql_client)
        db_cursor.execute(f"SELECT * FROM submission WHERE submission_id = {submission_id}")
        res = db_cursor.fetchall()
        
        res = date_helper.query_date_to_string(res)
        if len(res) == 0:
            raise ValueError()
        return res[0]
    
def GET_submission_history(team_id):
    with init_connection() as mysql_client:
        with init_cursor(mysql_client) as db_cursor:
            sql = f"""SELECT name, team_info, submit_date, prompt, image 
                    FROM user INNER JOIN prompts ON user.user_id = prompts.team_id
                            INNER JOIN submission ON prompts.prompt_id = submission.prompt_id
                    WHERE team_id = {team_id} AND submitted = 1
            """
            db_cursor.execute(sql)
            res = db_cursor.fetchall()

            if len(res) == 0:
                raise ValueError()
            
            res = date_helper.query_date_to_string(res)

            return res[0]

def GET_team_submission(team_id):
    with init_connection() as mysql_client:
        db_cursor = init_cursor(mysql_client)
        db_cursor.execute(f"""SELECT submission_id, submission.prompt_id, submit_date
                                FROM submission INNER JOIN prompts ON prompts.prompt_id = submission.prompt_id
                                WHERE prompts.team_id = {team_id}""")
        res = db_cursor.fetchall()
        
        res = date_helper.query_date_to_string(res)
        if len(res) == 0:
            raise ValueError()
        return res[0]

def GET_grader_assigned_submissions(grader_id):
    with init_connection() as mysql_client:
        db_cursor = init_cursor(mysql_client)
        
        sql = f"""SELECT assigned_submissions.submission_id, prompt, image, img_grader_id, prompt_grader_id, img_comment, prompt_comment, img_score, prompt_score, status, modified_date
                FROM assigned_submissions
                    INNER JOIN submission ON assigned_submissions.submission_id = submission.submission_id
                    INNER JOIN prompts ON prompts.prompt_id = submission.prompt_id
                WHERE img_grader_id = {grader_id}  OR prompt_grader_id = {grader_id}"""
        db_cursor.execute(sql)
        
        res = db_cursor.fetchall()
        
        res = date_helper.query_date_to_string(res)
        return res

def GET_assigned_submission(submission_id):
    with init_connection() as mysql_client:
        db_cursor = init_cursor(mysql_client)
        db_cursor.execute(f"SELECT * FROM assigned_submissions WHERE submission_id = {submission_id}")
        
        res = db_cursor.fetchall()
        
        res = date_helper.query_date_to_string(res)
        return res

def GET_all_assigned_submissions():
    with init_connection() as mysql_client:
        db_cursor = init_cursor(mysql_client)
        sql = """WITH q AS(
                    SELECT assigned_submissions.submission_id, name as team_name
                    FROM assigned_submissions 
                        INNER JOIN submission ON assigned_submissions.submission_id = submission.submission_id
                        INNER JOIN prompts ON prompts.prompt_id = submission.prompt_id
                        INNER JOIN user ON user_id = team_id
                )
                SELECT assigned_submissions.submission_id, team_name, img_grader_id, img.name as img_grader_name, prompt_grader_id, prompt.name as prompt_grader_name, img_comment, prompt_comment, img_score, prompt_score, status, modified_date
                FROM assigned_submissions
                    INNER JOIN user as img ON assigned_submissions.img_grader_id = img.user_id
                    INNER JOIN user as prompt ON assigned_submissions.prompt_grader_id = prompt.user_id
                    INNER JOIN q ON assigned_submissions.submission_id = q.submission_id;
                    """
        db_cursor.execute(sql)
        
        res = db_cursor.fetchall()
        
        res = date_helper.query_date_to_string(res)
        return res 
    
### Update ###
def UPDATE_user(user_id, update_data):
    with init_connection() as mysql_client:
        db_cursor = init_cursor(mysql_client)
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

def UPDATE_prompt(prompt_id):
    with init_connection() as mysql_client:
        db_cursor = init_cursor(mysql_client)
        db_cursor.execute(f"UPDATE prompts SET submitted = 1 WHERE prompt_id = {prompt_id}")
        mysql_client.commit()
    
def UPDATE_assigned_submission(submission_id, params:dict, update_time):
    with init_connection() as mysql_client:
        db_cursor = init_cursor(mysql_client)
        sql = f"""SELECT * FROM assigned_submissions WHERE submission_id = {submission_id}"""
        db_cursor.execute(sql)
        res = db_cursor.fetchall()        

        sql = """UPDATE assigned_submissions
                                SET """
        for key,value in params.items():
            if value:
                if type(value) == str:
                        sql += f" {key} = \"{value}\","
                else:
                    sql += f" {key} = {value},"

        sql += f"modified_date = \"{update_time}\" "
        sql += f"WHERE submission_id = {submission_id}"
        db_cursor.execute(sql)
        

        sql = f"""SELECT * FROM assigned_submissions WHERE submission_id = {submission_id}"""
        db_cursor.execute(sql)
        res = db_cursor.fetchall()
        obj_after_grade = date_helper.query_date_to_string(res)[0]
        if obj_after_grade['img_score']  and ['prompt_score']:
            sql = f"""UPDATE assigned_submissions
                    SET status = 1
                    WHERE submission_id = {submission_id}"""
            db_cursor.execute(sql)
        mysql_client.commit()
        
### DELETE ###
def DELETE_user(user_id):
    with init_connection() as mysql_client:
        db_cursor = init_cursor(mysql_client)
        
        user = GET_user(user_id)
        if user['group_id'] == 1:
            assigned_submisssions = GET_grader_assigned_submissions(user_id)
            for assigned_submission in assigned_submisssions:
                submission_id = assigned_submission['submission_id']
            sql = f"""UPDATE submission SET assigned = 0
                    WHERE submission_id = {submission_id}"""
            db_cursor.execute(sql)
        
        sql = f"DELETE FROM user WHERE user_id = {user_id}"
        db_cursor.execute(sql)
        mysql_client.commit()

def DELETE_all_ungraded_assigned_submissions():
    with init_connection() as mysql_client:
        db_cursor = init_cursor(mysql_client)
        
        sql = f"UPDATE submission SET assigned = 0 WHERE submission_id IN (SELECT submission_id FROM assigned_submissions WHERE status = 0)"
        db_cursor.execute(sql)
        
        sql = f"DELETE FROM assigned_submissions WHERE status = 0"
        db_cursor.execute(sql)
        
        mysql_client.commit()

def DELETE_assigned_submission(submission_id):
    with init_connection() as mysql_client:
        db_cursor = init_cursor(mysql_client)
        
        sql = f"DELETE FROM assigned_submissions WHERE submission_id = {submission_id}"
        db_cursor.execute(sql)
        
        sql = f"UPDATE submission SET assigned = 0 WHERE submission_id = {submission_id}"
        db_cursor.execute(sql)
        
        mysql_client.commit()

### Custom query ###
def execute_select(query):
    with init_connection() as mysql_client:
        db_cursor = init_cursor(mysql_client)
        try:
            db_cursor.execute(query)
            res = db_cursor.fetchall()        
        except Exception as e:
            return {"error": str(e)},401
        return res

def execute_insert(query):
    with init_connection() as mysql_client:
        db_cursor = init_cursor(mysql_client)
        try:
            db_cursor.execute(query)
            mysql_client.commit()
            res = "Insert success"        
        except Exception as e:
            return {"error": str(e)},401
        return res

def execute_update(query):
    with init_connection() as mysql_client:
        db_cursor = init_cursor(mysql_client)
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
