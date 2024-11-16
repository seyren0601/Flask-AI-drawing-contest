from DAL import db,model
from Helper import user
from datetime import datetime
### CREATE ###
def create_team(team_name):
    team = db.CREATE_team(team_name)
    return team

def create_user():
    username = f"usr{len(db.GET_all_users()):05}"    
    password = user.random_password()
    group_id = 3
    salt , hashed_pw = user.hash_password(password)    
    new_user = db.CREATE_user(username,group_id,salt,hashed_pw)
    return new_user

def image_generate(team_id,prompt):    
    image = model.image_generate(prompt)
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    submitted = 0
    
    db.CREATE_prompt(team_id,date_time,prompt,image,submitted)
    return image
### READ ###
def get_all_user():
    users = db.GET_all_users()
    return users

def get_user(user_id):
    user = db.GET_user(user_id)
    return user

def get_all_teams():
    teams = db.GET_all_teams()
    return teams

def get_team(team_id):
    team = db.GET_team(team_id)
    return team
