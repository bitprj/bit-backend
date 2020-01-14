from flask import (Blueprint, jsonify, request)
from flask_jwt_extended import create_access_token, set_access_cookies
from flask_restful import Resource
from flask_praetorian import auth_required, roles_required
from backend import api, db
from backend.authentication.schemas import user_form_schema
from backend.authentication.utils import create_user
from backend.authentication.decorators import user_exists
from backend.authentication.validators import check_user_existence
from backend.models import User

# Blueprint for users
authentication_bp = Blueprint("authentication", __name__)


# Class to create a user
class UserCreate(Resource):
    # Function to return data on a single user
    def post(self, user_type):
        form_data = request.get_json()
        errors = user_form_schema.validate(form_data)
        # If form data is not validated by the user_form_schema, then return a 500 error
        # else create the user and add it to the database
        if errors:
            return {
                       "message": "Missing or sending incorrect data to create a " + user_type + ". Double check the JSON data that it has everything needed to create a " + user_type + "."
                   }, 500
        else:
            user_already_exist = check_user_existence(form_data["username"])

            # If user exist in the database, then return an error message to
            # tell the user to choose a different email
            if user_already_exist:
                return {
                           "message": "Email already exists. Please choose another one."
                       }, 500
            else:
                user = create_user(user_type, form_data)

                # If the user_type is invalid then do not create the user
                if not user:
                    return {
                               "message": "Type of user does not exist."
                           }, 500

                db.session.add(user)
                db.session.commit()

        return {"message": user_type + " successfully created"}, 202


# Class to login in a user
class UserLoginHandler(Resource):
    method_decorators = [user_exists]

    # Function to login a user through a jwt token
    def post(self):
        form_data = request.get_json()
        username = form_data["username"]
        password = form_data["password"]
        user = User.query.filter_by(username=username, password=password).first()

        # Create the tokens we will be sending back to the user
        access_token = create_access_token(identity=username)
        resp = jsonify({"username": username,
                        "user_type": user.roles,
                        "logged_in": True})
        set_access_cookies(resp, access_token)

        return resp


# Class to logout a user
class UserLogoutHandler(Resource):
    # Function to invalidate the user's jwt token. This is used to log out the user
    # Use this to invalidate the current user's access token
    def delete(self):
        return {"access_token": None}, 200


class Protected(Resource):
    method_decorators = [auth_required]

    # This route is to check if the user is authenticated with a jwt token
    def get(self):
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


# Creates the routes for the classes
api.add_resource(UserCreate, "/users/<string:user_type>/create")
api.add_resource(UserLoginHandler, "/user/login")
api.add_resource(UserLogoutHandler, "/user/logout")
api.add_resource(Protected, "/protected")
api.add_resource(UserIsAdmin, "/isAdmin")
api.add_resource(UserIsStudent, "/isStudent")
api.add_resource(UserIsTeacher, "/isTeacher")
