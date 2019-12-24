from flask import (Blueprint, request)
from flask_praetorian.decorators import roles_accepted
from flask_restful import Resource
from backend import api, db
from backend.general_utils import get_user_id_from_token
from backend.models import Module, Student, Topic
from backend.modules.utils import vadlidate_module
from backend.prereqs.utils import assign_badge_prereqs
from backend.prereqs.validators import validate_activities, validate_badges, validate_modules
from backend.topics.schemas import topic_schema, topic_form_schema, topic_progress_schema
from backend.topics.utils import create_topic, edit_topic, get_topic_progress, validate_topic

# Blueprint for topics
topics_bp = Blueprint("topics", __name__)


# Class to Read, Update, and Destroy routes
class TopicData(Resource):
    # Function to return data on a single topic
    def get(self, topic_id):
        topic = Topic.query.get(topic_id)

        # If topic does not exists, then return a 404 error
        # else return the topic back to the user
        if not topic:
            return {"message": "Topic does not exist"}, 404
        else:
            return topic_schema.dump(topic)

    # Function to edit a topic
    def put(self, topic_id):
        topic = Topic.query.get(topic_id)

        # If topic does not exist, then return a 404 error
        # else edit a topic and edit it in the database
        if not topic:
            return {"message": "Topic does not exist"}, 404
        else:
            form_data = request.get_json()
            errors = topic_form_schema.validate(form_data)

            # If form data is not validated by the topic_schema, then return a 500 error
            # else edit the topic and save it to the database
            if errors:
                return {
                           "message": "Missing or sending incorrect data to edit a topic. Double check the JSON data that it has everything needed to edit a topic."
                       }, 500
            else:
                # Checks it the activity, badge, and module ids are valid before editing the topic
                activity_error = validate_activities(form_data["activity_prereqs"])
                badge_error = validate_badges(form_data["badge_prereqs"])
                module_error = validate_modules(form_data["modules"])
                module_prereqs_errror = validate_modules(form_data["modules"])

                if activity_error or badge_error or module_error or module_prereqs_errror:
                    return {
                               "message": "Activity or Badge or Module does not exist. Double check the arrays to check if the ids are valid in the database."
                           }, 500
                else:
                    edit_topic(topic, form_data)
                    db.session.commit()

                return {"message": "Topic successfully updated"}, 202

    # Function to delete a topic
    def delete(self, topic_id):
        topic = Topic.query.get(topic_id)

        # If topic does not exists, return a 404 error
        # else delete the topic and save to database
        if not topic:
            return {"message": "Topic does not exists"}, 404
        else:
            db.session.delete(topic)
            db.session.commit()

        return {"message": "Topic successfully deleted"}, 200


# Class to define topic creation
class TopicCreate(Resource):
    # Function to create a topic
    def post(self):
        form_data = request.get_json()
        errors = topic_form_schema.validate(form_data)

        # If form data is not validated by the topic_schema, then return a 500 error
        # else create the topic and add it to the database
        if errors:
            return {
                       "message": "Missing or sending incorrect data to create a topic. Double check the JSON data that it has everything needed to create a topic."
                   }, 500
        else:
            # Checks it the activity, badge, and module ids are valid before creating a topic
            activity_error = validate_activities(form_data["activity_prereqs"])
            badge_error = validate_badges(form_data["badge_prereqs"])
            module_error = validate_modules(form_data["modules"])
            module_prereqs_errror = validate_modules(form_data["modules"])

            if activity_error or badge_error or module_error or module_prereqs_errror:
                return {
                           "message": "Activity or Badge or Module does not exist. Double check the arrays to check if the ids are valid in the database."
                       }, 500
            else:
                topic = create_topic(form_data)
                db.session.add(topic)
                db.session.commit()
                assign_badge_prereqs(form_data["badge_prereqs"], topic, "Topic")
                db.session.commit()

            return {"message": "Topic successfully created"}, 202


# Class for topic progress
class TopicProgress(Resource):
    method_decorators = [roles_accepted("Student")]

    # Function to retrieve the module progress for a student given an id
    def get(self, topic_id):
        current_user_id = get_user_id_from_token()
        topic_error = validate_topic(topic_id)

        if topic_error:
            return {
                       "message": "Topic does not exist."
                   }, 500
        else:
            topic_progress = get_topic_progress(current_user_id, topic_id)
            return topic_progress_schema.dump(topic_progress)

    # Function to update the student's completed module
    def put(self, topic_id):
        current_user_id = get_user_id_from_token()
        student = Student.query.get(current_user_id)
        topic_error = validate_topic(topic_id)
        module_completed = request.get_json()
        module_id = module_completed["complete"]["id"]
        module_error = vadlidate_module(module_id)

        if topic_error or module_error:
            return {
                       "message": "Topic or Module does not exist."
                   }, 500
        else:
            module = Module.query.get(module_id)
            student.completed_modules.append(module)
            student.incomplete_modules.remove(module)
            db.session.commit()

        return {
                   "message": "Successfully updated student completed modules"
               }, 202


# Creates the routes for the classes
api.add_resource(TopicData, "/topics/<int:topic_id>")
api.add_resource(TopicCreate, "/topics/create")
api.add_resource(TopicProgress, "/topics/<int:topic_id>/progress")
