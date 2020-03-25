from flask import (Blueprint, jsonify, redirect, request, session)
from flask_jwt_extended import create_access_token, get_csrf_token, get_jwt_identity, jwt_required, set_access_cookies, \
    unset_jwt_cookies
from flask_restful import Resource
from backend import api, auth0, db, jwt, oauth, safe_url
from backend.authentication.utils import create_user, send_verification_email, store_user
from backend.badges.utils import create_student_badges
from backend.authentication.decorators import roles_required, user_exists, user_is_active, valid_user_form, \
    valid_user_type
from backend.models import Badge, User
from backend.modules.utils import create_module_progresses
from itsdangerous import SignatureExpired
from six.moves.urllib.parse import urlencode
import requests

# Blueprint for users
authentication_bp = Blueprint("authentication", __name__)


# Class to redirect to auth0
class UserAuth0(Resource):
    def get(self):
        return auth0.authorize_redirect(redirect_uri='http://localhost:5000/auth/callback')


# Class to logout using auth0
class UserAuth0Logout(Resource):
    def get(self):
        session.clear()
        params = {'returnTo': 'http://localhost:5000/auth', 'client_id': 'TW6496jNDAkANSIJwG1muLznFxz1Fj11'}
        return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


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


# Callback route to get data from auth0
class UserCallBack(Resource):
    def get(self):
        auth0.authorize_access_token()
        resp = auth0.get('userinfo')
        userinfo = resp.json()


        session['jwt_payload'] = userinfo
        session['profile'] = {
            'name': userinfo['name'],
            'image': userinfo['picture'],
            'username': userinfo['email']
        }

        # Hard coding this data for now
        userinfo["track_id"] = 1
        userinfo["location"] = "Davis"
        # I think is_active is now unneccessary
        userinfo["is_active"] = True 
        userinfo["password"] = "TemporaryPW"

        # If user doesn't exist store in db
        cur_user = User.query.filter_by(username=userinfo["email"]).first()
        if (cur_user is None):
            store_user(userinfo)

        return redirect('/')


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
        # re = requests.post("https://secure-escarpment-83921.herokuapp.com", json=form_data)
        # print(re.status_code)
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
        userinfo = session["profile"]["username"]
        return userinfo
        #return jsonify({"message": "pong"})


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    user = User.query.filter_by(username=identity).first()

    return {
        "roles": user.roles
    }


# Creates the routes for the classes
api.add_resource(UserAuth0, "/auth")
api.add_resource(UserAuth0Logout, "/auth/logout")
api.add_resource(UserAuthorize, "/confirm_email/<string:token>")
api.add_resource(UserCallBack, "/auth/callback")
api.add_resource(UserCreate, "/users/<string:user_type>/create")
api.add_resource(UserLoginHandler, "/user/login")
api.add_resource(UserLogoutHandler, "/user/logout")
api.add_resource(Protected, "/protected")
api.add_resource(UserIsAdmin, "/isAdmin")
api.add_resource(UserIsStudent, "/isStudent")
api.add_resource(UserIsTeacher, "/isTeacher")
api.add_resource(Ping, "/ping")