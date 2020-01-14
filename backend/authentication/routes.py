from flask import (Blueprint, jsonify, request)
from flask_jwt_extended import create_access_token, jwt_required, set_access_cookies, unset_jwt_cookies, \
    get_jwt_identity
from flask_restful import Resource
from backend import api, db, jwt
from backend.authentication.utils import create_user
from backend.authentication.decorators import user_exists, valid_user_form, roles_required
from backend.models import User

# Blueprint for users
authentication_bp = Blueprint("authentication", __name__)


# Class to create a user
class UserCreate(Resource):
    method_decorators = [valid_user_form]

    # Function to return data on a single user
    def post(self, user_type):
        if user_type == "Student" or user_type == "Teacher" or user_type == "Admin":
            form_data = request.get_json()
            user = create_user(user_type, form_data)

            db.session.add(user)
            db.session.commit()
        else:
            return {
                "message": "User type does not exist"
            }

        return {"message": user_type + " successfully created"}, 202


# Class to login in a user
class UserLoginHandler(Resource):
    method_decorators = [user_exists]

    # Function to login a user through a jwt token
    def post(self):
        form_data = request.get_json()
        username = form_data["username"]
        user = User.query.filter_by(username=username).first()

        # Create the tokens we will be sending back to the user
        access_token = create_access_token(identity=username)
        resp = jsonify({"username": username,
                        "user_type": user.roles,
                        "logged_in": True})
        set_access_cookies(resp, access_token)

        return resp


# Class to logout a user
class UserLogoutHandler(Resource):
    # This function works by deleting the jwt cookies associated with the user
    def delete(self):
        resp = jsonify({"logout": True})
        unset_jwt_cookies(resp)

        return resp


class Protected(Resource):
    method_decorators = [jwt_required]

    # This route is to check if the user is authenticated with a jwt token
    def get(self):
        username = get_jwt_identity()
        return jsonify({"message": "User is logged!"})


class UserIsAdmin(Resource):
    method_decorators = [roles_required("Admin")]

    # This route is used to validate if the user is an Admin
    def get(self):
        return jsonify({"message": "Admin logged in!"})


class UserIsStudent(Resource):
    method_decorators = [roles_required("Student")]

    # This route is used to validate if the user is a Student
    def get(self):
        return jsonify({"message": "Student logged in!"})


class UserIsTeacher(Resource):
    method_decorators = [roles_required("Teacher")]

    # This route is used to validate if the user is a Teacher
    def get(self):
        return jsonify({"message": "Teacher logged in!"})


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    user = User.query.filter_by(username=identity).first()

    return {
        "roles": user.roles
    }


# Creates the routes for the classes
api.add_resource(UserCreate, "/users/<string:user_type>/create")
api.add_resource(UserLoginHandler, "/user/login")
api.add_resource(UserLogoutHandler, "/user/logout")
api.add_resource(Protected, "/protected")
api.add_resource(UserIsAdmin, "/isAdmin")
api.add_resource(UserIsStudent, "/isStudent")
api.add_resource(UserIsTeacher, "/isTeacher")
