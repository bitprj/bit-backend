from flask import (Blueprint, request)
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from backend import api, db
from backend.activities.decorators import activity_exists, activity_exists_in_github, valid_activity_form
from backend.activities.schemas import activity_schema, activities_schema
from backend.activities.utils import create_activity, edit_activity
from backend.general_utils import create_schema_json
from backend.models import Activity

# Blueprint for activities
activities_bp = Blueprint("activities", __name__)


# Class for activity CRUD routes
class ActivityCRUD(Resource):

    # Function to create a activity
    @valid_activity_form
    def post(self):
        data = request.get_json()
        activity = create_activity(data)
        activity.content_url = create_schema_json(activity, "activity")

        db.session.add(activity)
        db.session.commit()

        return {"message": "Activity successfully created"}, 201

    # Function to edit an activity
    @valid_activity_form
    @activity_exists_in_github
    def put(self):
        data = request.get_json()
        activity = Activity.query.filter_by(filename=data["filename"]).first()
        edit_activity(activity, data)
        activity.content_url = create_schema_json(activity, "activity")

        db.session.commit()

        return {"message": "Activity successfully updated"}, 200

    # Function to delete a activity!!
    @activity_exists_in_github
    def delete(self):
        data = request.get_json()
        activity = Activity.query.filter_by(filename=data["filename"]).first()

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
        activity.cards.sort(key=lambda x: x.order)

        return activity_schema.dump(activity)


# Creates the routes for the classes
api.add_resource(ActivityCRUD, "/activities")
api.add_resource(ActivityFetchAll, "/activities/all")
api.add_resource(ActivityGetSpecific, "/activities/<int:activity_id>")
