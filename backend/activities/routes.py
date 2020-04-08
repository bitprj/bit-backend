from backend import api, db
from backend.activities.decorators import activity_exists, activity_exists_in_github, valid_activity_form
from backend.activities.schemas import ActivitySerializer
from backend.activities.utils import create_activity, edit_activity
from backend.general_utils import create_schema_json
from backend.models import Activity
from flask import (Blueprint, request)
from flask_jwt_extended import jwt_required
from flask_restful import Resource
<<<<<<< HEAD
from serpy import Serializer, IntField, StrField, MethodField, BoolField
=======
>>>>>>> 6fbb1cb8fc785094786229f311a2efcb0601a5ff

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
        activity.cards.sort(key=lambda x: x.order)
        create_schema_json(activity, "activities")
        db.session.commit()

        return {"message": "Activity successfully created"}, 201

    # Function to edit an activity
    @valid_activity_form
    @activity_exists_in_github
    def put(self):
        data = request.get_json()
        activity = Activity.query.filter_by(filename=data["filename"]).first()
        edit_activity(activity, data)
        activity.cards.sort(key=lambda x: x.order)
        create_schema_json(activity, "activities")
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


# This class is used to get a specific activity based on id
class ActivityGetSpecific(Resource):
    method_decorators = [jwt_required, activity_exists]

    def get(self, activity_id):
        activity = Activity.query.get(activity_id)
        activity.cards.sort(key=lambda x: x.order)

        return ActivitySerializer(activity).data


# Creates the routes for the classes
api.add_resource(ActivityCRUD, "/activities")
api.add_resource(ActivityGetSpecific, "/activities/<int:activity_id>")
