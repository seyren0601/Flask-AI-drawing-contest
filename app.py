from flask import Flask
from flask import request
from flask_restx import Api, Resource
from Controllers import controller

app = Flask(__name__)
api = Api(app)

### CREATE ###

### READ ###
@api.route("/user", methods=['GET', 'POST'])
class user(Resource):
    def get(self):
        users = controller.get_all_user()
        return users
    
@api.route("/team", methods=['GET'])
class team(Resource):
    def get(self, team_id):
        teams = controller.get_all_teams()
        return teams

### UPDATE ###

### DELETE ###

if __name__ == '__main__':
    app.run(debug=True)