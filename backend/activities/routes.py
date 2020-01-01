from flask import (Blueprint, request)
from flask_restful import Resource
from backend import api, db
from backend.activities.schemas import activities_schema
from backend.activities.utils import create_activity, edit_activity
from backend.models import Activity

# Blueprint for activities
activities_bp = Blueprint("activities", __name__)


# Class for activity CRUD routes
class ActivityCRUD(Resource):
    # Function to get all activities
    def get(self):
        activities = Activity.query.all()

        return activities_schema.dump(activities)

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
        edit_activity(contentful_data)

        db.session.commit()

        return {"message": "Activity successfully updated"}, 200


# This class is used to delete an activity with a POST request
class ActivityDelete(Resource):
    # Function to delete a activity!!
    def post(self):
        contentful_data = request.get_json()
        activity = Activity.query.filter_by(contentful_id=contentful_data["entityId"]).first()

        db.session.delete(activity)
        db.session.commit()

        return {"message": "Activity successfully deleted"}, 200


# Creates the routes for the classes
api.add_resource(ActivityCRUD, "/activities")
api.add_resource(ActivityDelete, "/activities/delete")

