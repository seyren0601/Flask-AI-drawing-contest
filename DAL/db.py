import mysql.connector
import os
import datetime
import json
import logging
import random
from Helper import date_helper
from dotenv import load_dotenv
from collections import defaultdict
load_dotenv()

db_host = os.environ["DB_HOST"]
db_user = os.environ["DB_USER"]
db_password = os.environ["DB_PASSWORD"]
db_database = os.environ["DB_DATABASE"]
def init_connection():
    mysql_client = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_database
    )    
    return mysql_client

def init_cursor(client):
    db_cursor = client.cursor(dictionary=True)

    return db_cursor

### CREATE ###
def CREATE_user(group_id,salt,hashed_pw,date_string):
    with init_connection() as mysql_client:
        db_cursor = init_cursor(mysql_client)
        query = """
            INSERT INTO user (group_id,salt, hashed_pw, register_date)
            VALUES (%s, %s,%s, %s)
        """
        db_cursor.execute(query, (group_id,salt,hashed_pw,date_string))
        mysql_client.commit()
    
        db_cursor.execute(f"SELECT * FROM user WHERE user_id = {db_cursor.lastrowid}")    
        user = db_cursor.fetchall()    
        user = date_helper.query_date_to_string(user)[0]
        user_id = user['user_id']
        username = "usr" + str(user_id).zfill(5)
        
        db_cursor.execute(f"UPDATE user SET username=\"{username}\" WHERE user_id = {user_id}")
        mysql_client.commit()
        
        db_cursor.execute(f"SELECT * FROM user WHERE user_id = {user_id}")
        user = db_cursor.fetchall()    
        user = date_helper.query_date_to_string(user)
        return user[0]

def CREATE_user_v2(insert_data):
    with init_connection() as mysql_client:
        db_cursor = init_cursor(mysql_client)
        params = []
        inserts = []
        for key , value in insert_data.items():
            if value is not None:
                inserts.append(f"{key}")
                params.append(value)    

        query = f"""
            INSERT INTO user ({', '.join(inserts)})
            VALUES ({','.join(['%s'] * len(params))})
        """
        db_cursor.execute(query,tuple(params))
        mysql_client.commit()
        
        db_cursor.execute(f"SELECT * FROM user WHERE user_id = {db_cursor.lastrowid}")    
        user = db_cursor.fetchall()    
        user = date_helper.query_date_to_string(user)[0]
        user_id = user['user_id']
        username = "usr" + str(user_id).zfill(5)
        
        db_cursor.execute(f"UPDATE user SET username=\"{username}\" WHERE user_id = {user_id}")
        mysql_client.commit()
    
        db_cursor.execute(f"SELECT * FROM user WHERE user_id = {user_id}")    
        user = db_cursor.fetchall()    
        user = date_helper.query_date_to_string(user)
        return user[0]

def CREATE_prompt(team_id,date_time,prompt,image):
    with init_connection() as mysql_client:
        db_cursor = init_cursor(mysql_client)
                
        query = """
            INSERT INTO prompts (team_id,date_time,prompt,image,submitted)
            VALUE (%s,%s,%s,%s, 0)
        """
        db_cursor.execute(query,(team_id,date_time,prompt,image))
        mysql_client.commit()

def CREATE_submission(prompt_id, submit_date):
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
            raise PermissionError("Submission limit exceeded")
        
        query = f"""
            INSERT INTO submission (submit_date,assigned)
            VALUE (\"{submit_date}\", 0)
        """
        db_cursor.execute(query)
        mysql_client.commit()

        db_cursor.execute(f"SELECT * FROM submission WHERE submission_id = {db_cursor.lastrowid}")
        submission = db_cursor.fetchall()
        date_helper.query_date_to_string(submission)
        return submission[0]

def CREATE_assigned_submission(**kwargs):
    with init_connection() as mysql_client:
        db_cursor = init_cursor(mysql_client)
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
            
        
def CREATE_randomly_assigned_submissions():
    with init_connection() as mysql_client:
        with init_cursor(mysql_client) as db_cursor:
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
    with init_connection() as mysql_client:
        db_cursor = init_cursor(mysql_client)
        db_cursor.execute("SELECT * FROM user")
        res = db_cursor.fetchall()
        res = date_helper.query_date_to_string(res)
        return res
    
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
    with init_connection() as mysql_client:
        db_cursor = init_cursor(mysql_client)
        db_cursor.execute(f"""SELECT team_id, name, prompt_id, date_time, prompt, image, submitted, submission_id
                            FROM user INNER JOIN prompts ON user.user_id = prompts.team_id
                            WHERE team_id = {team_id}
                        """)
        res = db_cursor.fetchall()
        
        res = date_helper.query_date_to_string(res)
        return res

def GET_prompt(prompt_id):
    with init_connection() as mysql_client:
        db_cursor = init_cursor(mysql_client)
        db_cursor.execute(f"SELECT * FROM prompts WHERE prompt_id = {prompt_id}")
        res = db_cursor.fetchall()
        res = date_helper.query_date_to_string(res)
        if len(res) == 0:
            raise ValueError()
        return res[0]

def GET_all_prompts():
    with init_connection() as mysql_client:
        db_cursor = init_cursor(mysql_client)
        db_cursor.execute(f"SELECT * FROM prompts")
        res = db_cursor.fetchall()
        
        res = date_helper.query_date_to_string(res)
        return res

def GET_all_submissions():
    with init_connection() as mysql_client:
        db_cursor = init_cursor(mysql_client)

        sql = f"""SELECT DISTINCT name as team_name, submission.submission_id, submit_date, assigned
                    FROM submission 
                        INNER JOIN prompts ON submission.submission_id = prompts.submission_id
                        INNER JOIN user ON user.user_id = prompts.team_id
                """

        db_cursor.execute(sql)
        res = db_cursor.fetchall()
        
        res = date_helper.query_date_to_string(res)
        submissions = []
        for response in res:
            sql = f"""SELECT prompt_id 
                        FROM prompts 
                        INNER JOIN submission ON prompts.submission_id = submission.submission_id
                        WHERE submission.submission_id = {response['submission_id']}
            """
            db_cursor.execute(sql)
            prompt_ids = db_cursor.fetchall()
            prompt1_id = prompt_ids[0]['prompt_id']
            prompt2_id = prompt_ids[1]['prompt_id']
            
            response_object = {
                    "team_name":response['team_name'],
                    "submission_id":response['submission_id'],
                    "prompt1_id":prompt1_id,
                    "prompt2_id":prompt2_id,
                    "submit_date":response['submit_date'],
                    "assigned":response['assigned']
            }
            
            submissions.append(response_object)
        return submissions
    
def GET_all_graded_submissions():
    with init_connection() as mysql_client:
        db_cursor = init_cursor(mysql_client)
        assigned_submissions = GET_all_assigned_submissions()

        graded_submissions = []

        for submission in assigned_submissions:
            if bool(submission['status']):
                submission_id = submission['submission_id']
                team_name = submission['team_name']
                total_score = sum(map(int, [submission['img1_score'], submission['img2_score'], submission['prompt1_score'], submission['prompt2_score']]))

                sql = f"SELECT prompt_id, image, prompt FROM prompts INNER JOIN submission ON prompts.submission_id = submission.submission_id WHERE submission.submission_id = {submission_id} ORDER BY prompt_id"
                db_cursor.execute(sql)
                res = db_cursor.fetchall()
                img1 = res[0]['image']
                img2 = res[1]['image']
                prompt1 = res[0]['prompt']
                prompt2 = res[1]['prompt']

                response = {
                    "team_name":team_name,
                    "img1":img1,
                    "img2":img2,
                    "prompt1":prompt1,
                    "prompt2":prompt2,
                    "total_score":total_score
                }

                graded_submissions.append(response)
        return graded_submissions

def GET_submission(submission_id):
    with init_connection() as mysql_client:
        db_cursor = init_cursor(mysql_client)
        db_cursor.execute(f"SELECT * FROM submission WHERE submission_id = {submission_id}")
        res = db_cursor.fetchall()
        
        res = date_helper.query_date_to_string(res)
        if len(res) == 0:
            raise ValueError()
        submission = res[0]
        
        sql = f"""SELECT prompt_id FROM prompts WHERE submission_id = {submission['submission_id']}
        """
        db_cursor.execute(sql)
        res = db_cursor.fetchall()
        prompt1 = res[0]
        prompt2 = res[1]
        
        response_object = {
            "submission_id":submission['submission_id'],
            "prompt1_id":prompt1['prompt_id'],
            "prompt2_id":prompt2['prompt_id'],
            "submit_date":submission['submit_date']
        }
        
        return response_object

def GET_team_submission(team_id):
    with init_connection() as mysql_client:
        db_cursor = init_cursor(mysql_client)
        db_cursor.execute(f"""SELECT submission.submission_id, prompt_id, submit_date
                                FROM submission INNER JOIN prompts ON prompts.submission_id = submission.submission_id
                                WHERE prompts.team_id = {team_id} ORDER BY prompt_id""")
        res = db_cursor.fetchall()
        res = date_helper.query_date_to_string(res)
        if len(res) == 0:
            raise ValueError()
        
        response_object = {
            "submission_id":res[0]['submission_id'],
            "prompt1_id":res[0]['prompt_id'],
            "prompt2_id":res[1]['prompt_id'],
            "submit_date":res[0]['submit_date']
        }
        
        return response_object
    
def GET_submission_history(team_id):
    with init_connection() as mysql_client:        
        sql = f"""SELECT name, team_info, submit_date, prompt, image 
                    FROM user INNER JOIN prompts ON user.user_id = prompts.team_id
                            INNER JOIN submission ON prompts.submission_id = submission.submission_id
                    WHERE team_id = {team_id} AND submitted = 1
            """
        db_cursor = init_cursor(mysql_client)
        db_cursor.execute(sql)
        res = db_cursor.fetchall()                        
        res = date_helper.query_date_to_string(res)        

        if len(res) == 0:
            raise ValueError()                                
        response_object = {
            "name":res[0]['name'],
            "team_info": res[0]['team_info'],
            "submit_date": res[0]['submit_date'],
            "prompt1":res[0]['prompt'],
            "prompt2":res[1]['prompt'],
            "image_1":res[0]['image'],
            "image_2":res[1]['image']
        }
        return response_object

def GET_grader_assigned_submissions(grader_id):
    with init_connection() as mysql_client:
        db_cursor = init_cursor(mysql_client)        
        sql = f"""
                SELECT distinct assigned_submissions.submission_id,
                    img_grader_id,
                    prompt_grader_id,prompt,image,
                    img1_comment, img2_comment,
                    prompt1_comment, prompt2_comment,
                    img1_score, img2_score, 
                    prompt1_score, prompt2_score, 
                    status, modified_date
                FROM assigned_submissions
                INNER JOIN submission ON assigned_submissions.submission_id = submission.submission_id
                INNER JOIN prompts ON prompts.submission_id = submission.submission_id
                WHERE img_grader_id = {grader_id}  OR prompt_grader_id = {grader_id}"""
        db_cursor.execute(sql)
        
        res = db_cursor.fetchall()
        res = date_helper.query_date_to_string(res)
        

        merged_data = defaultdict(lambda: {
            "submission_id": None,
            "prompt1": None,
            "prompt2": None,
            "image1": None,
            "image2": None,
            "img_grader_id": None,
            "prompt_grader_id": None,
            "img1_comment": None,
            "img2_comment": None,
            "prompt1_comment": None,
            "prompt2_comment": None,
            "img1_score": None,
            "img2_score": None,
            "prompt1_score": None,
            "prompt2_score": None,
            "status": None,
            "modified_date": None
        })
        for row in res:
            submission_id = row["submission_id"]
            entry = merged_data[submission_id]
            if entry["submission_id"] is None:
                entry.update({
                    "submission_id": submission_id,
                    "img_grader_id": row["img_grader_id"],
                    "prompt_grader_id": row["prompt_grader_id"],
                    "img1_comment": row["img1_comment"],
                    "img2_comment": row["img2_comment"],
                    "prompt1_comment": row["prompt1_comment"],
                    "prompt2_comment": row["prompt2_comment"],
                    "img1_score": row["img1_score"],
                    "img2_score": row["img2_score"],
                    "prompt1_score": row["prompt1_score"],
                    "prompt2_score": row["prompt2_score"],
                    "status": row["status"],
                    "modified_date": row["modified_date"]
                })      
            if entry["prompt1"] is None:
                entry.update({"prompt1": row["prompt"], "image1": row["image"]})
            elif entry["prompt2"] is None:
                entry.update({"prompt2": row["prompt"], "image2": row["image"]})
                
        response = list(merged_data.values())
        
        return response

def GET_assigned_submission(submission_id):
    with init_connection() as mysql_client:
        db_cursor = init_cursor(mysql_client)
        db_cursor.execute(f"SELECT * FROM assigned_submissions WHERE submission_id = {submission_id}")
        
        res = db_cursor.fetchall()
        
        res = date_helper.query_date_to_string(res)
        if len(res) == 0:
            raise ValueError
        return res[0]

def GET_all_assigned_submissions():
    with init_connection() as mysql_client:
        db_cursor = init_cursor(mysql_client)
        sql = """WITH q AS(
                    SELECT distinct assigned_submissions.submission_id, name as team_name
                    FROM assigned_submissions 
                        INNER JOIN submission ON assigned_submissions.submission_id = submission.submission_id
                        INNER JOIN prompts ON prompts.submission_id = submission.submission_id
                        INNER JOIN user ON user_id = team_id
                    )
                    SELECT assigned_submissions.submission_id, team_name, 
                            img_grader_id, img.name as img_grader_name, 
                            prompt_grader_id, prompt.name as prompt_grader_name, 
                            img1_comment, img2_comment,
                            prompt1_comment, prompt2_comment,
                            img1_score, img2_score, 
                            prompt1_score, prompt2_score, 
                            status, modified_date
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

def UPDATE_prompt(prompt_id, submission_id):
    with init_connection() as mysql_client:
        db_cursor = init_cursor(mysql_client)
        db_cursor.execute(f"UPDATE prompts SET submitted = 1 WHERE prompt_id = {prompt_id}")
        db_cursor.execute(f"UPDATE prompts SET submission_id = {submission_id} WHERE prompt_id = {prompt_id}")
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
        if obj_after_grade['img1_score']\
            and obj_after_grade['prompt1_score']\
            and obj_after_grade['img2_score']\
            and obj_after_grade['prompt2_score']:
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
            
            if len(assigned_submisssions) > 0:
                for assigned_submission in assigned_submisssions:
                    submission_id = assigned_submission['submission_id']                                   
                    sql = f"""UPDATE submission SET assigned = 0
                            WHERE submission_id = {submission_id}"""
                    db_cursor.execute(sql)
                    mysql_client.commit()
        elif user['group_id'] == 2:
            prompts = GET_team_prompts(user_id)
            for prompt in prompts:                
                if bool(prompt['submitted']):
                    submission_id = prompt["submission_id"]
                    sql = f"DELETE FROM submission WHERE submission_id = {submission_id}"
                    db_cursor.execute(sql)
                    mysql_client.commit()
                    break                                            
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
