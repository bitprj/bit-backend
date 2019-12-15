from flask import (Blueprint, request)
from flask_restful import Resource
from backend import api, db
from backend.badges.utils import create_badge, edit_badge
from backend.models import Badge, badge_schema

# Blueprint for badges
badges_bp = Blueprint("badges", __name__)


# Class to Read, Update, and Destroy routes
class BadgeData(Resource):
    # Function to return data on a single badge
    def get(self, badge_id):
        badge = Badge.query.get(badge_id)
        # If badge does not exists, then return a 404 error
        # else return the badge back to the user
        if not badge:
            return {"message": "Badge does not exist"}, 404
        else:
            return badge_schema.jsonify(badge)

    # Function to edit a badge
    def put(self, badge_id):
        badge = Badge.query.get(badge_id)

        # If badge does not exist, then return a 404 error
        # else edit a badge and edit it in the database
        if not badge:
            return {"message": "Badge does not exist"}, 404
        else:
            form_data = request.get_json()
            errors = badge_schema.validate(form_data)

            # If form data is not validated by the badge_schema, then return a 500 error
            # else edit the badge and save it to the database
            if errors:
                return {
                            "message": "Missing or sending incorrect data to edit a badge. Double check the JSON data that it has everything needed to create a badge."
                       }, 500
            else:
                edit_badge(badge, form_data)
                db.session.commit()

                return {"message": "Badge successfully updated"}, 202

    # Function to delete a badge
    def delete(self, badge_id):
        badge = Badge.query.get(badge_id)

        # If badge does not exists, return a 404 error
        # else delete the badge and save to database
        if not badge:
            return {"message": "Badge does not exists"}, 404
        else:
            db.session.delete(badge)
            db.session.commit()

        return {"message": "Badge successfully deleted"}, 200


# Class to define badge creation
class BadgeCreate(Resource):
    # Function to create a badge
    def post(self):
        form_data = request.get_json()
        errors = badge_schema.validate(form_data)
        # If form data is not validated by the badge_schema, then return a 500 error
        # else create the badge and add it to the database
        if errors:
            return {
                "message": "Missing or sending incorrect data to create a badge. Double check the JSON data that it has everything needed to create a badge."
            }, 500
        else:
            badge = create_badge(form_data)
            db.session.add(badge)
            db.session.commit()

            return {"message": "Badge successfully created"}, 202


# Creates the routes for the classes
api.add_resource(BadgeData, "/badges/<int:badge_id>")
api.add_resource(BadgeCreate, "/badges/create")
