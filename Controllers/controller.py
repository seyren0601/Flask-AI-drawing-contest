from DAL import db,model
from Helper import user
from datetime import datetime
### CREATE ###
def create_user():
    username = f"usr{len(db.GET_all_users()):05}"    
    password = user.random_password()
    group_id = 3
    salt , hashed_pw = user.hash_password(password)
    current_date = datetime.now()
    date_string = f"{current_date.year}-{current_date.month}-{current_date.day}"
    new_user = db.CREATE_user(username,group_id,salt,hashed_pw,date_string)
    return {'user_id':new_user['user_id'],'username':new_user['username'], 'password':password}

def create_prompt(team_id,prompt):
    image = model.image_generate(prompt)
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    submitted = 0
    
    db.CREATE_prompt(team_id,date_time,prompt,image,submitted)
    return image

def create_submission(prompt_id,video):
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    score = None
    submission = db.CREATE_submission(prompt_id,date_time,video,score)
    prompt = db.UPDATE_prompt(prompt_id)
    return submission
### READ ###
def get_all_user():
    users = db.GET_all_users()
    return users

def get_user(user_id):
    user = db.GET_user(user_id)
    return user

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
