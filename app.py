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
@api.route("/user/create",methods = ['GET'])
class user_create(Resource):
    def get(self):
        user = controller.create_user()
        return user

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
    
@api.route("/submission/create",methods=['POST'])
class submission_create(Resource):
    def post(self):
        parser = reqparse.RequestParser()        
        parser.add_argument('prompt_id',type=int,required=True,location='json')
        parser.add_argument('video',type=str,required=True,location='json')
        argument = parser.parse_args()
        
        prompt_id = argument['prompt_id']
        video = argument['video']
        submission = controller.create_submission(prompt_id,video)
        
        return submission
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

@api.route("/submission", methods=['GET'])
@api.param('submission_id')
@api.param('team_id')
class submission_read(Resource):
    def get(self):
        submission_id = request.args.get('submission_id')
        team_id = request.args.get('team_id')
        if submission_id:
            submission = controller.get_submission(submission_id)
            return submission
        if team_id:
            submission = controller.get_team_submission(team_id)
            return submission
        submissions = controller.get_all_submissions()
        return submissions
    
@api.route("/assigned_submissions", methods=['GET'])
@api.param('grader_id')
@api.param('submission_id')
class assigned_submissions(Resource):
    def get(self):
        grader_id = request.args.get('grader_id')
        assigner_id = request.args.get('assigner_id')
        submission_id = request.args.get('submission_id')
        if assigner_id:
            assigned_submissions = controller.get_assigner_assigned_submissions(assigner_id)
            return assigned_submissions
        if grader_id:
            assigned_submissions = controller.get_grader_assigned_submissions(grader_id)
            return assigned_submissions
        if submission_id:
            assigned_submission = controller.get_assigned_submission(submission_id)
            return assigned_submission
        all_assigned_submissions = controller.get_all_assigned_submissions()
        return all_assigned_submissions
        
### UPDATE ###
@api.route("/assigned_submission/update", methods=["POST"])
class assigned_submission_update(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('submission_id',type=int,required=True,location='json')
        parser.add_argument('status', type=int,required=True,location='json')
        parser.add_argument('comment', type=str,required=True,location='json', default="")
        parser.add_argument('score',type=float,required=True,location='json')
        argument = parser.parse_args()
        
        submission_id = argument['submission_id']
        status = argument['status']
        comment = argument['comment']
        score = argument['score']
        controller.update_assigned_submission(submission_id, status, comment, score)
        
        return Response(status=200)


### DELETE ###

if __name__ == '__main__':
    app.run(debug=True)