from backend import api
from backend.authentication.decorators import user_session_exists
from backend.users.decorators import user_exists
from backend.users.schemas import UserSerializer
from backend.models import User
from flask import Blueprint
from flask_restful import Resource

# Blueprint for users
user_bp = Blueprint("user", __name__)


# Class to handle information regarding the User model
class UserData(Resource):
    method_decorators = [user_session_exists, user_exists]

    def get(self, user_id):
        user = User.query.get(user_id)

        return UserSerializer(user).data


api.add_resource(UserData, "/users/<int:user_id>")
