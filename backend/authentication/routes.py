from flask import (Blueprint, g, jsonify, session)
from flask_restful import Resource
from backend import api, app, db, github
from backend.authentication.utils import create_user
from backend.authentication.decorators import access_token_exists, roles_required, user_session_exists
from backend.models import User

# Blueprint for users
authentication_bp = Blueprint("authentication", __name__)


@authentication_bp.route("/github-callback")
@access_token_exists
@github.authorized_handler
def authorized(access_token):
    oauth_user = None

    if oauth_user is None:
        oauth_user = User(github_access_token=access_token)

    g.user = oauth_user
    github_user = github.get("/user")
    github_emails = github.get("/user/emails")
    existing_user = User.query.filter_by(github_id=github_user["id"]).first()

    if existing_user:
        oauth_user = existing_user
    else:
        oauth_user = create_user(github_user, github_emails)
        db.session.add(oauth_user)

    db.session.commit()
    session["profile"] = {
        "id": oauth_user.id,
        "roles": oauth_user.roles
    }
    g.user = oauth_user

    return {
               "message": "Login Successful"
           }, 200


# Class to handle OAuth login for users
class UserOAuthLoginHandler(Resource):
    def get(self):
        if session.get("profile", None) is None:
            return github.authorize(scope="read:user, read:repo, user:email")
        else:
            return {
                       "message": "Already logged in"
                   }, 403


# Class to handle OAuth logout for users
class UserOAuthLogoutHandler(Resource):
    method_decorators = [user_session_exists]

    def get(self):
        session.pop("profile", None)

        return {
                   "message": "Successfully logged out"
               }, 200


class Protected(Resource):
    method_decorators = [user_session_exists]

    # This route is to check if the user is authenticated through sessions
    def get(self):
        user_data = session["profile"]

        return jsonify(
            {
                "message": "User is logged!",
                "user_type": user_data["roles"]
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


@app.before_request
def before_request():
    g.user = None
    if "id" in session:
        g.user = User.query.get(session["id"])


@app.after_request
def after_request(response):
    db.session.remove()
    return response


@github.access_token_getter
def token_getter():
    oauth_user = g.user
    if oauth_user is not None:
        return oauth_user.github_access_token


# Creates the routes for the classes
api.add_resource(Ping, "/ping")
api.add_resource(Protected, "/protected")
api.add_resource(UserIsAdmin, "/isAdmin")
api.add_resource(UserIsStudent, "/isStudent")
api.add_resource(UserIsTeacher, "/isTeacher")
api.add_resource(UserOAuthLoginHandler, "/login")
api.add_resource(UserOAuthLogoutHandler, "/logout")

