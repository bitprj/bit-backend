from flask import (Blueprint, request)
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from backend import api, db
from backend.badges.decorators import badge_delete, badge_exists, badge_exists_in_contentful
from backend.badges.schemas import badge_schema
from backend.badges.utils import create_badge, edit_badge
from backend.models import Badge


# Blueprint for badges
badges_bp = Blueprint("badges", __name__)


# Class for badge CRUD routes
class BadgeCRUD(Resource):
    method_decorators = [badge_exists_in_contentful]

    # Function to create a badge
    def post(self):
        contentful_data = request.get_json()
        badge = create_badge(contentful_data)

        db.session.add(badge)
        db.session.commit()

        return {"message": "Badge successfully created"}, 201

    # Function to edit an badge
    def put(self):
        contentful_data = request.get_json()
        badge = Badge.query.filter_by(contentful_id=contentful_data["entityId"]).first()
        edit_badge(badge, contentful_data)

        db.session.commit()

        return {"message": "Badge successfully updated"}, 200


# This class is used to delete an badge with a POST request
class BadgeDelete(Resource):
    method_decorators = [badge_delete]

    # Function to delete a badge!!
    def post(self):
        contentful_data = request.get_json()
        badge = Badge.query.filter_by(contentful_id=contentful_data["entityId"]).first()

        db.session.delete(badge)
        db.session.commit()

        return {"message": "Badge successfully deleted"}, 200


# Function to get a specific Badge based on badge id
class BadgeGetSpecific(Resource):
    method_decorators = [badge_exists, jwt_required]

    def get(self, badge_id):
        badge = Badge.query.get(badge_id)

        return badge_schema.dump(badge)


# Creates the routes for the classes
api.add_resource(BadgeCRUD, "/badges")
api.add_resource(BadgeDelete, "/badges/delete")
api.add_resource(BadgeGetSpecific, "/badges/<int:badge_id>")
