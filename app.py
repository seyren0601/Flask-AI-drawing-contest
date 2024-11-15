from flask import Flask
from flask_restx import Api, Resource
from Controllers import controller

app = Flask(__name__)
api = Api(app)

### CREATE ###
@api.route("/user/create",methods = ['POST'])
class user_create(Resource):
    def post(self):
        user = controller.create_user()
        return user
### READ ###
@api.route("/user", methods=['GET', 'POST'])
class user(Resource):
    def get(self):
        users = controller.get_all_user()
        return users
# @app.route("/user", methods=['GET', 'POST'])
# def user():    
#     users = controller.get_all_user()
#     return users

### UPDATE ###

### DELETE ###

if __name__ == '__main__':
    app.run(debug=True)