from flask import (Blueprint, jsonify, request)
from flask_jwt_extended import create_access_token, get_csrf_token, get_jwt_identity, jwt_required, set_access_cookies, \
    unset_jwt_cookies
from flask_restful import Resource
from backend import api, db, jwt, safe_url
from backend.authentication.utils import create_user, send_verification_email
from backend.badges.utils import create_student_badges
from backend.authentication.decorators import roles_required, user_exists, user_is_active, valid_user_form, \
    valid_user_type
from backend.models import Badge, User
from backend.modules.utils import create_module_progresses
from itsdangerous import SignatureExpired
import requests

# Blueprint for users
authentication_bp = Blueprint("authentication", __name__)


class UserAuthorize(Resource):
    # Route to confirm that the email is real
    def get(self, token):
        email = None

        try:
            email = safe_url.loads(token, salt='email-confirm', max_age=3600)
        except SignatureExpired:
            return {
                       "message": "Your email token has expired. Go send a new one."
                   }, 500

        user = User.query.filter_by(username=email).first()
        user.is_active = True
        db.session.commit()

        return {
                   "message": "Your email has been verified. You can login now."
               }, 200


# Class to create a user
class UserCreate(Resource):
    method_decorators = [valid_user_form, valid_user_type]

    # Function to return data on a single user
    def post(self, user_type):
        form_data = request.get_json()
        user = create_user(user_type, form_data)

        db.session.add(user)
        db.session.commit()

        if user_type == "Student":
            badges = Badge.query.all()
            create_module_progresses(user.incomplete_modules, user)
            create_student_badges(badges, user)
            db.session.commit()
        send_verification_email(user.username)

        return {"message": user_type + " successfully created"}, 202


# Class to login in a user
class UserLoginHandler(Resource):
    method_decorators = [user_exists]

    # Function to login a user through a jwt token
    @user_is_active
    def post(self):
        form_data = request.get_json()
        username = form_data["username"]
        user = User.query.filter_by(username=username).first()
        s = requests.post("https://916b196c.ngrok.io/login", json=form_data)
        # Create the tokens we will be sending back to the user
        access_token = create_access_token(identity=username)
        resp = jsonify({"username": username,
                        "user_type": user.roles,
                        "csrf_token": get_csrf_token(access_token),
                        })
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
        user = User.query.filter_by(username=username).first()

        return jsonify(
            {
                "message": "User is logged!",
                "user_type": user.roles
            }
        )


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


class Ping(Resource):
    def get(self):
        return jsonify({"message": "pong"})


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    user = User.query.filter_by(username=identity).first()

    return {
        "roles": user.roles
    }


# Creates the routes for the classes
api.add_resource(UserAuthorize, "/confirm_email/<string:token>")
api.add_resource(UserCreate, "/users/<string:user_type>/create")
api.add_resource(UserLoginHandler, "/user/login")
api.add_resource(UserLogoutHandler, "/user/logout")
api.add_resource(Protected, "/protected")
api.add_resource(UserIsAdmin, "/isAdmin")
api.add_resource(UserIsStudent, "/isStudent")
api.add_resource(UserIsTeacher, "/isTeacher")
api.add_resource(Ping, "/ping")
