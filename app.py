from flask import Flask
from Controllers import controller

app = Flask(__name__)

### CREATE ###

### READ ###
@app.route("/user", methods=['GET', 'POST'])
def user():
    users = controller.get_all_user()
    return users

### UPDATE ###

### DELETE ###