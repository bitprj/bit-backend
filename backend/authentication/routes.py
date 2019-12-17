from flask import (Blueprint, jsonify, request)
from flask_restful import Resource
from flask_praetorian import auth_required
from backend import api, db, guard
from backend.authentication.schemas import user_form_schema, user_login_schema
from backend.authentication.utils import create_user
from backend.authentication.validators import check_user_existence

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
class UserSessionHandler(Resource):
    # Function to login a user through a jwt token
    def post(self):
        form_data = request.get_json()
        errors = user_login_schema.validate(form_data)

        # If form data is not validated by the user_form_schema, then return a 500 error
        # else proceed to check if the user exists
        if errors:
            return {
                       "message": "Missing or sending incorrect login data. Double check the JSON data that it has everything needed to login."
                   }, 500
        else:
            username = form_data["username"]
            password = form_data["password"]
            user = guard.authenticate(username, password)
            token = guard.encode_jwt_token(user)

        return {"message": "Successfully logged in!", "access_token": token}, 200


class Protected(Resource):
    method_decorators = [auth_required]

    def get(self):
        return jsonify({"message": "Welcome!"})


class Open(Resource):
    def get(self):
        return jsonify({"message": "Anyone can visit"})


# Creates the routes for the classes
api.add_resource(UserCreate, "/users/<string:user_type>/create")
api.add_resource(UserSessionHandler, "/user/login")
api.add_resource(Protected, "/protected")
api.add_resource(Open, "/open")
