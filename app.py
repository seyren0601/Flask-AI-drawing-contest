from flask import Flask, Response,jsonify
from flask import request
from flask_cors import CORS
from flask_restx import reqparse,fields
from flask_restx import Api, Resource
from Controllers import controller
from Helper import server
import os

# def init_app():
#     """Initialize the core application."""
#     app = Flask(__name__)

#     with app.app_context():
#         with open("user_credentials.csv", "w+") as f:
#             for i in range(50):
#                 user = controller.create_user(2)
#                 f.write(f"{user['username']},{user['password']}\n")

#         return app
# app = init_app()

app = Flask(__name__)
api = Api(app)
CORS(app)

### CREATE ###
@api.route("/user/create",methods = ['GET','POST'])
class user_create(Resource):
    def get(self):
        try:
            bearer_token = request.headers['Authorization']
        except:
            return Response(status=400, response="Authorization not found")
        if not server.server_authentication(bearer_token):
            return Response(status=403)

        arg = request.args.get('group_id')
        if arg:
            group_id = int(arg)
        else:
            group_id = 2
        try:
            user = controller.create_user(group_id)
            return user
        except ValueError:
            return Response(status=400, response="Group id invalid")
        
    def post(self):
        try:
            bearer_token = request.headers['Authorization']
        except:
            return Response(status=400, response="Authorization not found")
        if not server.server_authentication(bearer_token):
            return Response(status=403)

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
        try:
            bearer_token = request.headers['Authorization']
        except:
            return Response(status=400, response="Authorization not found")
        if not server.server_authentication(bearer_token):
            return Response(status=403)

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
        try:
            bearer_token = request.headers['Authorization']
        except:
            return Response(status=400, response="Authorization not found")
        if not server.server_authentication(bearer_token):
            return Response(status=403)

        parser = reqparse.RequestParser()
        parser.add_argument('prompt1_id',type=int,required=True,location='json')
        parser.add_argument('prompt2_id',type=int,required=True,location='json')
        argument = parser.parse_args()
        prompt1_id = argument['prompt1_id']
        prompt2_id = argument['prompt2_id']
        
        try:
            submission = controller.create_submission(prompt1_id, prompt2_id)
        except PermissionError as e:
            return Response(status=400, response=str(e))
        return submission
    
@api.route("/assigned_submission/create",methods=["POST", "GET"])
class submission_assigned(Resource):
    def post(self):
        try:
            bearer_token = request.headers['Authorization']
        except:
            return Response(status=400, response="Authorization not found")
        if not server.server_authentication(bearer_token):
            return Response(status=403)

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
        try:
            bearer_token = request.headers['Authorization']
        except:
            return Response(status=400, response="Authorization not found")
        if not server.server_authentication(bearer_token):
            return Response(status=403)

        assigned_submissions = controller.create_assigned_submission()
        return assigned_submissions
    

### READ ###
@api.route("/user", methods=['GET'])
@api.param('user_id')
@api.param('group_id')
class user_read(Resource):
    def get(self):
        try:
            bearer_token = request.headers['Authorization']
        except:
            return Response(status=400, response="Authorization not found")
        if not server.server_authentication(bearer_token):
            return Response(status=403)

        user_id = request.args.get('user_id')
        group_id = request.args.get('group_id')
        if user_id:
            try:
                user = controller.get_user(user_id)
                return user
            except ValueError:
                return Response(status=400,response="User not found")            
        elif group_id : 
            user = controller.get_user_by_group(group_id)
            return user
        else:
            users = controller.get_all_user()
            return users
        
@api.route("/user/authenticate", methods=['POST'])
class user_login(Resource):
    def post(self):
        try:
            bearer_token = request.headers['Authorization']
        except:
            return Response(status=400, response="Authorization not found")
        if not server.server_authentication(bearer_token):
            return Response(status=403)

        parser = reqparse.RequestParser()
        parser.add_argument('username',type=str,required=True,location='json')
        parser.add_argument('password',type=str,required=True,location='json')
        arguments = parser.parse_args()
        
        username = arguments['username']
        password = arguments['password']
        user_id,group_id = controller.user_authenticate(username, password)
        if user_id != None and group_id != None:
            return {'user_id':user_id,'group_id':group_id}
        else:
            return Response(status=401, response="Failed Authentication")
    
        
@api.route("/prompts", methods=['GET'])
@api.param('team_id')
@api.param('prompt_id')
class prompts_read(Resource):
    def get(self):
        try:
            bearer_token = request.headers['Authorization']
        except:
            return Response(status=400, response="Authorization not found")
        if not server.server_authentication(bearer_token):
            return Response(status=403)

        team_id = request.args.get('team_id')
        prompt_id = request.args.get('prompt_id')
        if team_id:
            prompts = controller.get_team_prompts(team_id)
            return prompts
        if prompt_id:
            try:
                prompt = controller.get_prompt(prompt_id)
                return prompt
            except ValueError:
                return Response(status=400,response="Prompt not found")  
        prompts = controller.get_all_prompts()
        return prompts

@api.route("/submission", methods=['GET'])
@api.param('submission_id')
@api.param('team_id')
class submission_read(Resource):
    def get(self):
        try:
            bearer_token = request.headers['Authorization']
        except:
            return Response(status=400, response="Authorization not found")
        if not server.server_authentication(bearer_token):
            return Response(status=403)

        submission_id = request.args.get('submission_id')
        team_id = request.args.get('team_id')
        if submission_id:
            try:
                submission = controller.get_submission(submission_id)
                return submission
            except ValueError:
                return Response(status=400,response="Submission not found")
        if team_id:
            try:            
                submission = controller.get_team_submission(team_id)
                return submission
            except ValueError as e:
                return Response(status=400,response="Team or submission not found")
        submissions = controller.get_all_submissions()
        return submissions

@api.route("/submission/history", methods=['GET'])
@api.param('team_id')
class submission_history(Resource):
    def get(self):
        try:
            bearer_token = request.headers['Authorization']
        except:
            return Response(status=400, response="Authorization not found")
        if not server.server_authentication(bearer_token):
            return Response(status=403)

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
        try:
            bearer_token = request.headers['Authorization']
        except:
            return Response(status=400, response="Authorization not found")
        if not server.server_authentication(bearer_token):
            return Response(status=403)

        submission_id = request.args.get('submission_id')
        grader_id = request.args.get('grader_id')
        if grader_id:
            assigned_submissions = controller.get_grader_assigned_submissions(grader_id)
            return assigned_submissions
        if submission_id:
            try:
                assigned_submission = controller.get_assigned_submission(submission_id)
                return assigned_submission
            except ValueError:
                return Response(status=400, response='Assigned submission not found')
        all_assigned_submissions = controller.get_all_assigned_submissions()
        return all_assigned_submissions

@api.route("/query",methods=["POST"])
class query(Resource):
    def post(self):
        try:
            bearer_token = request.headers['Authorization']
        except:
            return Response(status=400, response="Authorization not found")
        if not server.server_authentication(bearer_token):
            return Response(status=403)

        parser = reqparse.RequestParser()
        parser.add_argument('query',type=str,required=True,location='json')
        argument = parser.parse_args()
        query = argument['query']
        data = controller.execute_query(query)
        return data
my_model = api.model('GradedSubmission ', {
    'team_name': fields.String(description='Tên đội thi',example='Đội Siêu Nhân'),
    'school_name': fields.String(description='Tên trường',example='Trường XYZ'),
    'img1': fields.String(description='Ảnh nộp thứ 1',example='chuỗi base64 của ảnh thứ 1'),
    "img2": fields.String(description='Ảnh nộp thứ 2',example='chuỗi base64 của ảnh thứ 2'),
    'img1_id': fields.Integer(description='Id của ảnh 1',example=1),
    'img2_id': fields.Integer(description='Id của ảnh 2',example=2),
    "prompt1": fields.String(description='Câu prompt hình 1',example='Vẽ con rồng'),
    "prompt2": fields.String(description='Câu prompt hình 2',example='Vẽ con rắn'),
    "total_score": fields.Integer(description='Tổng điểm',example=27)
})
@api.route("/graded_submissions", methods=['GET'])
#@api.response(400, 'Authorization not found')
#@api.response(403, "Forbidden ")
@api.response(200, "Success and return list of graded submissions",[my_model])
@api.route("/graded_submissions", methods=['GET'])
class graded_submissions(Resource):
    def get(self):
        try:
            bearer_token = request.headers['Authorization']
        except:
            return Response(status=400, response="Authorization not found")
        if not server.server_authentication(bearer_token):
            return Response(status=403)

        graded_submissions = controller.get_all_graded_submissions()
        return graded_submissions
    
@api.route("/all_submissions", methods=['GET'])
class all_submissions(Resource):
    def get(self):
        try:
            bearer_token = request.headers['Authorization']
        except:
            return Response(status=400, response="Authorization not found")
        if not server.server_authentication(bearer_token):
            return Response(status=403)
        
        all_submissions = controller.get_all_submissions_requested()
        return all_submissions

@api.route("/prompts/count", methods=["GET"])
class prompt_count(Resource):
    def get(self):
        try:
            bearer_token = request.headers['Authorization']
        except:
            return Response(status=400, response="Authorization not found")
        if not server.server_authentication(bearer_token):
            return Response(status=403)
        
        user_id = request.args.get('user_id')

        if user_id != None:
            try:
                prompt_count = controller.get_prompt_count(user_id)
                return prompt_count
            except ValueError:
                return Response(status=400, response="Invalid user_id")
        else:
            return Response(status=400, response="Invalid user_id")                
### UPDATE ###
@api.route("/user/update",methods=["POST"])
class user_update(Resource):
    def post(self):
        try:
            bearer_token = request.headers['Authorization']
        except:
            return Response(status=400, response="Authorization not found")
        if not server.server_authentication(bearer_token):
            return Response(status=403)

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
        try:
            bearer_token = request.headers['Authorization']
        except:
            return Response(status=400, response="Authorization not found")
        if not server.server_authentication(bearer_token):
            return Response(status=403)

        parser = reqparse.RequestParser()
        parser.add_argument('submission_id',type=int,required=True,location='json')
        parser.add_argument('img1_score',type=float,required=False,location='json')
        parser.add_argument('img2_score',type=float,required=False,location='json')
        parser.add_argument('prompt1_score',type=float,required=False,location='json')
        parser.add_argument('prompt2_score',type=float,required=False,location='json')
        parser.add_argument('img1_comment', type=str,required=False,location='json', default="")
        parser.add_argument('img2_comment', type=str,required=False,location='json', default="")
        parser.add_argument('prompt1_comment', type=str,required=False,location='json', default="")
        parser.add_argument('prompt2_comment', type=str,required=False,location='json', default="")
        
        argument = parser.parse_args()
        
        submission_id = argument['submission_id']
        img1_score = argument['img1_score']
        prompt1_score = argument['prompt1_score']
        img1_comment = argument['img1_comment']
        prompt1_comment = argument['prompt1_comment']
        
        img2_score = argument['img2_score']
        prompt2_score = argument['prompt2_score']
        img2_comment = argument['img2_comment']
        prompt2_comment = argument['prompt2_comment']
        try:
            controller.update_assigned_submission(submission_id, img1_score,prompt1_score, img1_comment, prompt1_comment,
                                                                 img2_score,prompt2_score, img2_comment, prompt2_comment)
        except ValueError:
            return Response(status=400, response="Grade already exists")
        except PermissionError:
            return Response(status=400, response="Submission already graded")
        
        
        return Response(status=200)


### DELETE ###
@api.route("/user/delete", methods=['DELETE'])
class user_delete(Resource):
    def delete(self):
        try:
            bearer_token = request.headers['Authorization']
        except:
            return Response(status=400, response="Authorization not found")
        if not server.server_authentication(bearer_token):
            return Response(status=403)

        user_id = request.args.get('user_id')
        if user_id != None:
            try:
                controller.delete_user(user_id)
            except ValueError:
                return Response(status=400, response="Invalid user_id")
        else:
            return Response(status=400, response="Invalid user_id")
        return Response(status=200)

@api.route("/assigned_submission/delete", methods=['DELETE'])
class assigned_submission_update(Resource):
    def delete(self):
        try:
            bearer_token = request.headers['Authorization']
        except:
            return Response(status=400, response="Authorization not found")
        if not server.server_authentication(bearer_token):
            return Response(status=403)
            
        submission_id = request.args.get('submission_id')
        if submission_id:
            controller.delete_assigned_submission(submission_id)
        else:
            controller.delete_all_ungraded_assigned_submissions()
            
        return Response(status=200)

if __name__ == '__main__':
    app.run("0.0.0.0")