from flask import (Blueprint, request)
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from backend import api, db
from backend.activities.decorators import activity_exists, activity_exists_in_github, valid_activity_form
from backend.activities.schemas import activity_schema, activities_schema
from backend.activities.utils import create_activity, delete_cards, edit_activity
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

        db.session.add(activity)
        db.session.commit()

        return {"message": "Activity successfully created"}, 201

    # Function to edit an activity
    @valid_activity_form
    @activity_exists_in_github
    def put(self):
        data = request.get_json()
        activity = Activity.query.filter_by(github_id=data["github_id"]).first()
        edit_activity(activity, data)

        db.session.commit()

        return {"message": "Activity successfully updated"}, 200

    # Function to delete a activity!!
    @activity_exists_in_github
    def delete(self):
        data = request.get_json()
        activity = Activity.query.filter_by(github_id=data["github_id"]).first()
        # delete_cards(activity.cards)

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
