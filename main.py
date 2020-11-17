# reqparse is used for parsing the form data
# marshal_with is used for serialization
# abort is used for aborting the session of database
from flask_restful import Api, Resource, abort, reqparse, fields, marshal_with
from app import app
from db_config import db
from models import UserModel

# Api instance
api = Api(app)

# Serializer
resource_fields = {
    'id': fields.Integer,
    'fName': fields.String,
    'lName': fields.String,
    'email': fields.String
}

# Parsing the form data for post and put method
user_args = reqparse.RequestParser()
user_args.add_argument("fName", type=str, help="First Name of the user is mendetory", required=True)
user_args.add_argument("lName", type=str, help="Last Name of the user")
user_args.add_argument("email", type=str, help="email of the user is mendetory", required=True)

# Parsing the form data for patch method
user_patch_args = reqparse.RequestParser()
user_patch_args.add_argument("fName", type=str, help="First Name of the user is mendetory")
user_patch_args.add_argument("lName", type=str, help="Last Name of the user")
user_patch_args.add_argument("email", type=str, help="email of the user is mendetory")

# Crud operations on a particular user
class User(Resource):
    @marshal_with(resource_fields)
    def get(self, user_id):
        result = UserModel.query.filter_by(id=user_id).first()
        if not result:
            abort(404, message="Could not find user with that id")
        return result
        
    @marshal_with(resource_fields)
    def post(self, user_id):
        args = user_args.parse_args()
        result = UserModel.query.filter_by(id=user_id).first()
        if result:
            abort(409, message="User already exists")

        user = UserModel(id=user_id, fName=args['fName'], lName=args['lName'], email=args['email'])
        db.session.add(user)
        db.session.commit()
        return user, 201

    @marshal_with(resource_fields)
    def put(self, user_id):
        args = user_args.parse_args()
        result = UserModel.query.filter_by(id=user_id).first()
        if not result:
            abort(404, message="User doesn't exists, can not update")
        
        result.fName = args['fName']
        result.lName = args['lName']
        result.email = args['email']
        
        db.session.commit()
        return result

    @marshal_with(resource_fields)
    def patch(self, user_id):
        args = user_patch_args.parse_args()
        result = UserModel.query.filter_by(id=user_id).first()
        if not result:
            abort(404, message="User doesn't exists, can not update")

        if args['fName']:
            result.fName = args['fName']
        if args['lName']:
            result.lName = args['lName']
        if args['email']:
            result.email = args['email']

        db.session.commit()

        return result


    def delete(self, user_id):
        result = UserModel.query.filter_by(id=user_id).first()
        if not result:
            abort(404, message="User doesn't exists, can not delete")
        
        db.session.delete(result)
        db.session.commit()
        return '', 204

# crud operations on whole list of users
class UserList(Resource):
    @marshal_with(resource_fields)
    def get(self):
        result = UserModel.query.all()
        if not result:
            abort(404, message="No Users found")
        return result

# Adding routes to Resource
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserList, "/users")

# Running Application
if __name__ == "__main__":
    app.run(debug=True)
