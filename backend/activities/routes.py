from flask import (Blueprint, json, request)
from flask_restful import Resource
from backend import api, db
from backend.activities.schemas import activity_schema, activity_file_schema
from backend.activities.utils import create_activity, edit_activity
from backend.models import Activity

# Blueprint for activities
activities_bp = Blueprint("activities", __name__)


# Class to Read, Update, and Destroy routes
class ActivityData(Resource):
    # Function to return data on a single activity
    def get(self, activity_id):
        activity = Activity.query.get(activity_id)

        # If activity does not exists, then return a 404 error
        # else return the activity back to the user
        if not activity:
            return {"message": "Activity does not exist"}, 404
        else:
            return activity_schema.dump(activity)

    # Function to edit a activity
    def put(self, activity_id):
        activity = Activity.query.get(activity_id)

        # If activity does not exist, then return a 404 error
        # else edit a activity and edit it in the database
        if not activity:
            return {"message": "Activity does not exist"}, 404
        else:
            activity_data = request.get_json()
            errors = activity_schema.validate(activity_data)

            # If form data is not validated by the activity_schema, then return a 500 error
            # else edit the activity and save it to the database
            if errors:
                return {
                           "message": "Missing or sending incorrect data to edit an activity. Double check the JSON data that it has everything needed to edit an activity."
                       }, 500
            else:
                edit_activity(activity, activity_data["activity_adjustment"])
                db.session.commit()

                return {"message": "Activity successfully updated"}, 202

    # Function to delete a activity
    def delete(self, activity_id):
        activity = Activity.query.get(activity_id)

        # If activity does not exists, return a 404 error
        # else delete the activity and save to database
        if not activity:
            return {"message": "Activity does not exist"}, 404
        else:
            db.session.delete(activity)
            db.session.commit()

        return {"message": "Activity successfully deleted"}, 200


# Class to define activity creation
class ActivityCreate(Resource):
    # Function to create a activity
    def post(self):
        form_data = request.form
        file_data = request.files
        errors = activity_schema.validate(form_data)
        file_errors = activity_file_schema.validate(file_data)

        if errors or file_errors:
            return {
                       "message": "Missing or sending incorrect data to create an activity. Double check the JSON data that it has everything needed to create an activity."
                   }, 500
        else:
            print(type(form_data["badge_prereqs"]))
            # activity = create_activity(form_data, file_data)
            # db.session.add(activity)
            # db.session.commit()

        return {"message": "Activity successfully created"}, 202


# Creates the routes for the classes
api.add_resource(ActivityData, "/activities/<int:activity_id>")
api.add_resource(ActivityCreate, "/activities/create")
