from flask import (Blueprint, jsonify, request)
from flask_restful import Resource
from backend import api, app, bcrypt, db
from backend.models import User
from backend.users.schemas import user_form_schema
from backend.users.utils import create_admin
import datetime
import jwt

# Blueprint for users
users_bp = Blueprint("users", __name__)


# Class to create a user
class AdminCreate(Resource):
    # Function to return data on a single user
    def post(self):
        form_data = request.get_json()
        errors = user_form_schema.validate(form_data)
        # If form data is not validated by the user_schema, then return a 500 error
        # else create the user and add it to the database
        if errors:
            return {
                       "message": "Missing or sending incorrect data to create an user. Double check the JSON data that it has everything needed to create an user."
                   }, 500
        else:
            admin = create_admin(form_data)
            db.session.add(admin)
            db.session.commit()

            return {"message": "User successfully created"}, 202


# Class to login in a user
class UserSessionHandler(Resource):
    # Function to login a user through a jwt token
    def post(self):
        form_data = request.get_json()
        errors = user_form_schema.validate(form_data)

        # If form data is not validated by the user_form_schema, then return a 500 error
        # else proceed to check if the user exists
        if errors:
            return {
                       "message": "Missing or sending incorrect data to create an user. Double check the JSON data that it has everything needed to create an user."
                   }, 500
        else:
            user = User.query.filter_by(email=form_data["email"]).first()

            # Checks if the user exists and if the password matches the email given
            # else return a 500 error
            if not user and not bcrypt.check_password_hash(user.password, form_data["password"]):
                return {
                           "message": "User does not exist or password does not match email."
                       }, 500
            else:
                token = jwt.encode(
                    {"public_id": user.public_id, "expiration": datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config["SECRET_KEY"])
                return jsonify({"token": token.decode("UTF-8")})

    # Creates the routes for the classes
    api.add_resource(AdminCreate, "/admins/create")
