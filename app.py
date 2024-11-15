from flask import Flask
from Controllers import controller

app = Flask(__name__)

### CREATE ###
@app.route("/user/create",methods = ['POST'])
def create_user():
    user = controller.create_user()
    return user
### READ ###
@app.route("/user", methods=['GET', 'POST'])
def user():    
    users = controller.get_all_user()
    return users

### UPDATE ###

### DELETE ###