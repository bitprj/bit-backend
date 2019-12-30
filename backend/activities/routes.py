from flask import (Blueprint, request)
from flask_restful import Resource
from backend import api, db
from backend.activities.utils import create_activity, get_activity
from backend.models import Activity

# Blueprint for activities
activities_bp = Blueprint("activities", __name__)


# Class to Read and Destroy routes
class ActivityData(Resource):
    # Function to return data on a single activity
    def get(self):
        contentful_data = request.get_json()
        activity = get_activity(contentful_data)

        # If activity does not exists, then return a 404 error
        # else return the activity back to the user
        if not activity:
            return {"message": "Activity does not exist"}, 404
        else:
            return {"contentful_id": activity.contentful_id}, 200

    # Function to create a activity
    def post(self):
        contentful_data = request.get_json()
        activity = create_activity(contentful_data)
        db.session.add(activity)
        db.session.commit()

        return {"message": "Activity successfully created"}, 202

    # Function to delete a activity
    def put(self):
        contentful_data = request.get_json()
        activity = Activity.query.filter_by(contentful_id=contentful_data["entityId"]).first()
        db.session.delete(activity)
        db.session.commit()

        return {"message": "Activity successfully deleted"}, 200


# Creates the routes for the classes
api.add_resource(ActivityData, "/activities")
