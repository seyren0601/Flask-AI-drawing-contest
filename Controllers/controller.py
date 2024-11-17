from DAL import db,model
from Helper import user
from datetime import datetime
### CREATE ###
def create_user():
    
    username = f"usr{len(db.GET_all_users()):05}"    
    password = user.random_password()
    group_id = 2
    salt , hashed_pw = user.hash_password(password)
    current_date = datetime.now()
    date_string = f"{current_date.year}-{current_date.month}-{current_date.day}"
    new_user = db.CREATE_user(username,group_id,salt,hashed_pw,date_string)    
    return {'user_id':new_user['user_id'],'username':new_user['username'], 'password':password}

def create_user_v2(name,school_name,grade,phone_number,email,team_info):
    username = f"usr{len(db.GET_all_users()):05}"    
    password = user.random_password()
    group_id = 2
    salt , hashed_pw = user.hash_password(password)
    current_date = datetime.now()
    date_string = f"{current_date.year}-{current_date.month}-{current_date.day}"

    insert_data ={
        "username": username,
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
    image = model.image_generate(prompt)
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    submitted = 0    
    db.CREATE_prompt(team_id,date_time,prompt,image,submitted)
    return image

def create_submission(prompt_id,video):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
    assigned = 0  
    submission = db.CREATE_submission(prompt_id,date_time,video,assigned)    
    prompt = db.UPDATE_prompt(prompt_id)
    return submission

def create_assigned_submission(submission_id, img_grader_id, video_grader_id, prompt_grader_id):
    assigned_submission = db.CREATE_assigned_submission(submission_id=submission_id, 
                                                        img_grader_id=img_grader_id, 
                                                        video_grader_id=video_grader_id, 
                                                        prompt_grader_id=prompt_grader_id)
    return assigned_submission

def create_assigned_submission():
    assigned_submissions = db.CREATE_assigned_submission()
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

    return None

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

def get_grader_assigned_submissions(grader_id):
    assigned_submissions = db.GET_grader_assigned_submissions(grader_id)
    return assigned_submissions

def get_assigned_submission(submission_id):
    assigned_submission = db.GET_assigned_submission(submission_id)
    return assigned_submission
    
def get_all_assigned_submissions():
    assigned_submissions = db.GET_all_assigned_submissions()
    return assigned_submissions

### UPDATE ###
def update_user(user_id,name,username,email,phonenumber,new_password,team_info):
    print(new_password)
    current_user = get_user(user_id)[0]
    salt = current_user['salt'].encode("utf-8")
    if new_password:      
        hashed_pw = user.hash_password(new_password,salt)[1]  
        print(f"Update hashed_pw: {hashed_pw}")                            
    else:        
        hashed_pw = current_user['hashed_pw']
    update_data = {
        "name": name,
        "username": username,
        "email":email,
        "phone_number":phonenumber,        
        "hashed_pw":hashed_pw,
        "team_info":team_info
    }
    db.UPDATE_user(user_id,update_data)

def update_assigned_submission(submission_id, img_score, video_score, prompt_score, img_comment, video_comment, prompt_comment):
    update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    params = {
        "img_score":img_score, 
        "video_score":video_score, 
        "prompt_score":prompt_score, 
        "img_comment":img_comment,
        "video_comment":video_comment,
        "prompt_comment":prompt_comment
    }
    db.UPDATE_assigned_submission(submission_id, params, update_time)


### DELETE ###