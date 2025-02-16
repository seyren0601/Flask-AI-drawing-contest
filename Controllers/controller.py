from DAL import db,model
from Helper import user
from datetime import datetime
import time
import base64
### CREATE ###
def create_user(group_id):
    password = user.random_password()
    if group_id > 2 or group_id < 0:
        raise ValueError
    salt , hashed_pw = user.hash_password(password)
    current_date = datetime.now()
    date_string = f"{current_date.year}-{current_date.month}-{current_date.day}"
    new_user = db.CREATE_user(group_id,salt,hashed_pw,date_string)    
    return {'user_id':new_user['user_id'],'username':new_user['username'], 'password':password}

def create_user_v2(name,school_name,grade,phone_number,email,team_info):
    password = user.random_password()
    group_id = 2
    salt , hashed_pw = user.hash_password(password)
    current_date = datetime.now()
    date_string = f"{current_date.year}-{current_date.month}-{current_date.day}"

    insert_data ={
        "group_id": group_id,
        "salt": salt,
        "hashed_pw": hashed_pw,
        "register_date":date_string,
        "name":name,
        "school_name":school_name,
        "grade":grade,
        "phone_number":phone_number,
        "email":email,
        "team_info": team_info
    }
    new_user = db.CREATE_user_v2(insert_data)
    return {'user_id':new_user['user_id'],'username':new_user['username'], 'password':password}

def create_prompt(team_id,prompt):
    team_prompts = get_team_prompts(team_id)
    
    if len(team_prompts) == 10:
        raise PermissionError
    
    image = model.image_generate(prompt)
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db.CREATE_prompt(team_id,date_time,prompt,image)
    return image

def create_submission(prompt1_id, prompt2_id):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    submission = db.CREATE_submission(prompt1_id, date_time)
    db.UPDATE_prompt(prompt1_id, submission['submission_id'])
    db.UPDATE_prompt(prompt2_id, submission['submission_id'])
    return submission

def create_assigned_submission(**kwargs):
    if len(kwargs.items()) > 0:
        assigned_submission = db.CREATE_assigned_submission(submission_id=kwargs['submission_id'], 
                                                            img_grader_id=kwargs['img_grader_id'],                                                             
                                                            prompt_grader_id=kwargs['prompt_grader_id'])
        return assigned_submission
    else:
        assigned_submissions = db.CREATE_randomly_assigned_submissions()
        return assigned_submissions

def execute_query(query):   
    match query.split():
        case ["SELECT", *rest]:
            result = db.execute_select(query)        
        case ["INSERT", *rest]:
            result = db.execute_insert(query)    
        case ["UPDATE", *rest]:
            result = db.execute_update(query)         
        # case ["DELETE", *rest]:
        #     result = "DELETE in query"
    return result
            
### READ ###
def get_all_user():
    users = db.GET_all_users()
    return users

def get_user(user_id):
    user = db.GET_user(user_id)    
    return user

def get_user_by_group(group_id):
    user = db.Get_user_by_group(group_id)
    return user

def user_authenticate(username, password):
    query_res = db.GET_user_authentication(username)
    if len(query_res) == 0:
        return None
    user_authentication = query_res[0]
    salt = user_authentication['salt'].encode('utf-8')
    hashed_pw = user_authentication['hashed_pw'].encode('utf-8')
    
    user_id = user_authentication['user_id']
    group_id = user_authentication['group_id']
    # print(f"Login hashed_pw: {user.hash_password(password, salt)[1]}")      
    if user.hash_password(password, salt)[1] == hashed_pw:
        return user_id,group_id

    return (None, None)

def get_team_prompts(team_id):
    prompts = db.GET_team_prompts(team_id)
    return prompts

def get_prompt(prompt_id):
    prompt = db.GET_prompt(prompt_id)
    return prompt

def get_all_prompts():
    prompts = db.GET_all_prompts()
    return prompts

def get_all_submissions():
    submissions = db.GET_all_submissions()
    return submissions

def get_team_submission(team_id):
    submission = db.GET_team_submission(team_id)
    return submission

def get_submission(submission_id):
    submission = db.GET_submission(submission_id)
    return submission

def get_submission_history(team_id):
    submission_history = db.GET_submission_history(team_id)
    return submission_history

def get_grader_assigned_submissions(grader_id):
    assigned_submissions = db.GET_grader_assigned_submissions(grader_id)
    return assigned_submissions

def get_assigned_submission(submission_id):
    assigned_submission = db.GET_assigned_submission(submission_id)
    return assigned_submission
    
def get_all_assigned_submissions():
    assigned_submissions = db.GET_all_assigned_submissions()
    return assigned_submissions

def get_prompt_count(user_id):
    prompt_count = db.Get_prompt_count(user_id)
    return prompt_count
### UPDATE ###
def update_user(user_id,name,username,email,school_name,grade,phonenumber,new_password,team_info):   
    current_user = get_user(user_id)
    salt = current_user['salt'].encode("utf-8")
    if new_password:      
        hashed_pw = user.hash_password(new_password,salt)[1]                                    
    else:        
        hashed_pw = current_user['hashed_pw']
    update_data = {
        "name": name,
        "username": username,
        "email":email,
        "school_name": school_name,
        "grade": grade,
        "phone_number":phonenumber,        
        "hashed_pw":hashed_pw,
        "team_info":team_info
    }
    db.UPDATE_user(user_id,update_data)
    update_user = db.GET_user(user_id)
    return update_user


def update_assigned_submission(submission_id, img1_score,prompt1_score, img1_comment, prompt1_comment,
                                                img2_score,prompt2_score, img2_comment, prompt2_comment):
    update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    params = {
        "img1_score":img1_score,
        "prompt1_score":prompt1_score,
        "img1_comment":img1_comment,
        "prompt1_comment":prompt1_comment,
        
        "img2_score":img2_score,
        "prompt2_score":prompt2_score,
        "img2_comment":img2_comment,
        "prompt2_comment":prompt2_comment
    }
    db.UPDATE_assigned_submission(submission_id, params, update_time)


### DELETE ###
def delete_user(user_id):
    user_id = db.DELETE_user(user_id)

def delete_assigned_submission(submission_id):
    db.DELETE_assigned_submission(submission_id)
    
def delete_all_ungraded_assigned_submissions():
    db.DELETE_all_ungraded_assigned_submissions()
    
### REQUESTED CONTROLLERS ###
def get_all_submissions_requested(page, limit):
    submissions = db.GET_all_submissions_requested(page, limit)
    return submissions

def get_all_graded_submissions():
    graded_submissions = db.GET_all_graded_submissions()
    return graded_submissions

def get_prompt_image(prompt_id):
    image_base64 = db.GET_prompt_image(prompt_id)
    
    image = base64.b64decode(image_base64)
    return image

def get_prompt_info(prompt_id):
    response = db.GET_prompt_info(prompt_id)
    return response