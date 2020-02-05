from flask import (Blueprint, request)
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from backend import api, db
from backend.activities.decorators import activity_delete, activity_exists, activity_exists_in_contentful
from backend.activities.schemas import activity_schema, activities_schema
from backend.activities.utils import create_activity, delete_cards, edit_activity
from backend.models import Activity

# Blueprint for activities
activities_bp = Blueprint("activities", __name__)


# Class for activity CRUD routes
class ActivityCRUD(Resource):
    method_decorators = [activity_exists_in_contentful]

    # Function to create a activity
    def post(self):
        contentful_data = request.get_json()
        activity = create_activity(contentful_data)

        db.session.add(activity)
        db.session.commit()

        return {"message": "Activity successfully created"}, 201

    # Function to edit an activity
    def put(self):
        contentful_data = request.get_json()
        activity = Activity.query.filter_by(contentful_id=contentful_data["entityId"]).first()
        edit_activity(activity, contentful_data)

        db.session.commit()

        return {"message": "Activity successfully updated"}, 200


# This class is used to delete an activity with a POST request
class ActivityDelete(Resource):
    method_decorators = [activity_delete]

    # Function to delete a activity!!
    def post(self):
        contentful_data = request.get_json()
        activity = Activity.query.filter_by(contentful_id=contentful_data["entityId"]).first()
        delete_cards(activity.cards)

        db.session.delete(activity)
        db.session.commit()

        return {"message": "Activity successfully deleted"}, 200


# Class to get all tracks
class ActivityFetchAll(Resource):
    method_decorators = [jwt_required]

    # Function to get all activities
    def get(self):
        activities = Activity.query.all()

        return activities_schema.dump(activities)


# This class is used to get a specific activity based on id
class ActivityGetSpecific(Resource):
    method_decorators = [jwt_required, activity_exists]

    def get(self, activity_id):
        activity = Activity.query.get(activity_id)

        return activity_schema.dump(activity)


# Creates the routes for the classes
api.add_resource(ActivityCRUD, "/activities")
api.add_resource(ActivityFetchAll, "/activities/all")
api.add_resource(ActivityDelete, "/activities/delete")
api.add_resource(ActivityGetSpecific, "/activities/<int:activity_id>")
