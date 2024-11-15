from flask import Flask
from flask import request
from flask_restx import Api, Resource
from Controllers import controller

app = Flask(__name__)
api = Api(app)

### CREATE ###

### READ ###
@api.route("/user", methods=['GET', 'POST'])
@api.param('user_id')
class user(Resource):
    def get(self):
        user_id = request.args.get('user_id')
        if user_id:
            user = controller.get_user(user_id)
            return user
        else:
            users = controller.get_all_user()
            return users
    
@api.route("/team", methods=['GET'])
@api.param('team_id')
class team(Resource):
    def get(self):
        team_id = request.args.get('team_id')
        if team_id:
            team = controller.get_team(team_id)
            return team
        else:
            teams = controller.get_all_teams()
            return teams

### UPDATE ###

### DELETE ###

if __name__ == '__main__':
    app.run(debug=True)