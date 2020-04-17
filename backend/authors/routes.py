from backend import api, db, git
from backend.models import Author
from flask import Blueprint, request
from flask_restful import Resource

# Blueprint for activities
authors_bp = Blueprint("authors", __name__)


# Class for activity CRUD routes
class AuthorCRUD(Resource):
    # Route to create an Author
    def post(self):
        data = request.get_json()
        # Only create Author if username exists
        if git.get_user(data["username"]):
            author = Author(username=data["username"])
            db.session.add(author)
            db.session.commit()

        return {
                   "message": "Author created"
               }, 201


api.add_resource(AuthorCRUD, "/authors")
