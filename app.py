from flask import Flask, Response,jsonify
from flask import request
from flask_cors import CORS
from flask_restx import reqparse
from flask_restx import Api, Resource
from Controllers import controller
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
import json


class Base(DeclarativeBase):
    pass

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:porsche0601@localhost/ai_drawing_contest" # To be hidden
db.init_app(app)
api = Api(app)
CORS(app)

with app.app_context():
    db.create_all()
    
class User(db.Model):
    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    
    def toJSON(self):
        return {
            "user_id":self.user_id, 
            "username":self.username,
            "email":self.email
        }

### CREATE ###
@api.route("/user/create",methods = ['GET','POST'])
class user_create(Resource):
    def get(self):
        user = controller.create_user()
        return user
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name',type=str,required=True,location='json')
        parser.add_argument('school_name',type=str,required=False,location='json')
        parser.add_argument('grade',type=str,required=False,location='json')
        parser.add_argument('phone_number',type=str,required=True,location='json')
        parser.add_argument('email',type=str,required=True,location='json')
        parser.add_argument('team_info',type=str,required=True,location='json')

        argument = parser.parse_args()

        name = argument['name']
        school_name = argument['school_name']
        grade = argument['grade']
        phone_number = argument['phone_number']
        email = argument['email']
        team_info = argument['team_info']

        user = controller.create_user_v2(name,school_name,grade,phone_number,email,team_info)
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
        try:
            image = controller.create_prompt(team_id,prompt)
        except PermissionError:
            return Response(status=400, response="Prompt limit exceeded.")
        return image
    
@api.route("/submission/create",methods=['POST'])
class submission_create(Resource):
    def post(self):
        parser = reqparse.RequestParser()        
        parser.add_argument('prompt_id',type=int,required=True,location='json')        
        argument = parser.parse_args()        
        prompt_id = argument['prompt_id']        
        
        try:
            submission = controller.create_submission(prompt_id)
        except PermissionError as e:
            return Response(status=400, response=str(e))
        return submission
    
@api.route("/assigned_submission/create",methods=["POST", "GET"])
class submission_assigned(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("submission_id",type=int,required=True,location='json')
        parser.add_argument("img_grader_id",type=int,required=True,location='json')        
        parser.add_argument("prompt_grader_id",type=int,required=True,location='json')

        argument = parser.parse_args()
        submission_id = argument["submission_id"]
        img_grader_id = argument["img_grader_id"]        
        prompt_grader_id = argument["prompt_grader_id"]

        assigned_submission = controller.create_assigned_submission(submission_id=submission_id, 
                                                                    img_grader_id=img_grader_id,                                                                     
                                                                    prompt_grader_id=prompt_grader_id)
        return assigned_submission
    
    def get(self):
        assigned_submissions = controller.create_assigned_submission()
        return assigned_submissions
    

### READ ###
@api.route("/user", methods=['GET'])
@api.param('user_id')
@api.param('group_id')
class user_read(Resource):
    def get(self):
        user_id = request.args.get('user_id')
        group_id = request.args.get('group_id')
        if user_id:
            user = controller.get_user(user_id)
            return user
        elif group_id : 
            user = controller.get_user_by_group(group_id)
            return user
        else:
            users = db.session.query(User)
            return [user.toJSON() for user in users]
        
@api.route("/user/authenticate", methods=['POST'])
class user_login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username',type=str,required=True,location='json')
        parser.add_argument('password',type=str,required=True,location='json')
        arguments = parser.parse_args()
        
        username = arguments['username']
        password = arguments['password']
        user_id,group_id = controller.user_authenticate(username, password)
        if user_id and group_id:
            return {'user_id':user_id,'group_id':group_id}
        else:
            return Response(status=401, response="Failed Authentication")
    
        
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

@api.route("/submission/history", methods=['GET'])
@api.param('team_id')
class submission_history(Resource):
    def get(self):
        team_id = request.args.get('team_id')
        if team_id:
            try:
                submission_history = controller.get_submission_history(team_id)
                return submission_history
            except ValueError:
                return Response(status=400, response="Unable to fetch submission history")
        else:
            return Response(status=400, response='team_id argument not found')

@api.route("/assigned_submissions", methods=['GET'])
@api.param('grader_id')
@api.param('submission_id')
class assigned_submissions(Resource):
    def get(self):
        submission_id = request.args.get('submission_id')
        grader_id = request.args.get('grader_id')
        if grader_id:
            assigned_submissions = controller.get_grader_assigned_submissions(grader_id)
            return assigned_submissions
        if submission_id:
            assigned_submission = controller.get_assigned_submission(submission_id)
            return assigned_submission
        all_assigned_submissions = controller.get_all_assigned_submissions()
        return all_assigned_submissions

@api.route("/query",methods=["POST"])
class query(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('query',type=str,required=True,location='json')
        argument = parser.parse_args()
        query = argument['query']
        data = controller.execute_query(query)
        return data   
### UPDATE ###
@api.route("/user/update",methods=["POST"])
class user_update(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id',type=int,required=True,location='json')
        parser.add_argument('name',type=str,required=False,location='json')
        parser.add_argument('username',type=str,required=False,location='json')
        parser.add_argument('email',type=str,required=False,location='json')
        parser.add_argument('school_name',type=str,required=False,location='json')
        parser.add_argument('grade',type=str,required=False,location='json')
        parser.add_argument('phonenumber',type=str,required=False,location='json')
        parser.add_argument('password',type=str,required=False,location='json')
        parser.add_argument('team_info',type=str,required=False,location='json')
        argument = parser.parse_args()
        #########################
        user_id  = argument['user_id']
        name = argument['name']
        username = argument['username']
        email = argument['email']
        school_name = argument['school_name']
        grade = argument['grade']
        phonenumber = argument['phonenumber']
        new_password = argument['password']
        team_info = argument['team_info']
        ########################
        update_user = controller.update_user(user_id,name,username,email,school_name,grade,phonenumber,new_password,team_info)

        return jsonify(update_user)

@api.route("/assigned_submission/update", methods=["POST"])
class assigned_submission_update(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('submission_id',type=int,required=True,location='json')
        parser.add_argument('img_score',type=float,required=False,location='json')        
        parser.add_argument('prompt_score',type=float,required=False,location='json')
        parser.add_argument('img_comment', type=str,required=False,location='json', default="")        
        parser.add_argument('prompt_comment', type=str,required=False,location='json', default="")
        
        argument = parser.parse_args()
        
        submission_id = argument['submission_id']
        img_score = argument['img_score']        
        prompt_score = argument['prompt_score']
        img_comment = argument['img_comment']        
        prompt_comment = argument['prompt_comment']
        try:
            controller.update_assigned_submission(submission_id, img_score,prompt_score, img_comment, prompt_comment)
        except ValueError:
            return Response(status=400, response="Grade already exists")
        except PermissionError:
            return Response(status=400, response="Submission already graded")
        
        
        return Response(status=200)


### DELETE ###
@api.route("/assigned_submission/delete", methods=['DELETE'])
class assigned_submission_update(Resource):
    def delete(self):
        submission_id = request.args.get('submission_id')
        if submission_id:
            controller.delete_assigned_submission(submission_id)
        else:
            controller.delete_all_ungraded_assigned_submissions()
            
        return Response(status=200)

if __name__ == '__main__':
    app.run(debug=True)