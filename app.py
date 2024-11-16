from flask import Flask, Response
from flask import request
from flask_cors import CORS
from flask_restx import reqparse
from flask_restx import Api, Resource
from Controllers import controller


app = Flask(__name__)
api = Api(app)
CORS(app)

### CREATE ###
@api.route("/user/create",methods = ['POST'])
class user_create(Resource):
    def post(self):
        user = controller.create_user()
        return user
        
@api.route("/team/create", methods=['POST'])
class team_create(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('team_name', type=str, required=True, location='json')
        argument = parser.parse_args()
        
        team_name = argument['team_name']
        team = controller.create_team(team_name)
        
        return team

@api.route("/prompt/create",methods=['POST'])
class prompt_create(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('team_id',type=int,required=True,location='json')
        parser.add_argument('prompt',type=str,required=True,location='json')
        argument = parser.parse_args()

        team_id = argument['team_id']
        prompt = argument['prompt']

        image = controller.create_prompt(team_id,prompt)
        return image
### READ ###
@api.route("/user", methods=['GET'])
@api.param('user_id')
class user_read(Resource):
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
class team_read(Resource):
    def get(self):
        team_id = request.args.get('team_id')
        if team_id:
            team = controller.get_team(team_id)
            return team
        else:
            teams = controller.get_all_teams()
            return teams
        
@api.route("/prompts", methods=['GET'])
@api.param('team_id')
@api.param('prompt_id')
class prompts_read(Resource):
    def get(self):
        team_id = request.args.get('team_id')
        prompt_id = request.args.get('prompt_id')
        if team_id:
            prompts = controller.get_team_prompts(team_id)
            return prompts
        if prompt_id:
            prompt = controller.get_prompt(prompt_id)
            return prompt
        prompts = controller.get_all_prompts()
        return prompts

### UPDATE ###

### DELETE ###

if __name__ == '__main__':
    app.run(debug=True)