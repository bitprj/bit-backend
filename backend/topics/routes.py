from flask import (Blueprint, request)
from flask_praetorian.decorators import roles_accepted
from flask_restful import Resource
from backend import api, db
from backend.general_utils import get_user_id_from_token
from backend.models import Module, Student, Topic
from backend.modules.utils import validate_module
from backend.topics.decorators import topic_delete, topic_exists, topic_exists_in_contentful
from backend.topics.schemas import topic_schema, topic_progress_schema
from backend.topics.utils import create_topic, delete_topic, edit_topic, get_topic_progress, validate_topic

# Blueprint for topics
topics_bp = Blueprint("topics", __name__)


# Class for topic CRUD routes
class TopicCRUD(Resource):
    method_decorators = [topic_exists_in_contentful]

    # Function to create a topic
    def post(self):
        contentful_data = request.get_json()
        topic = create_topic(contentful_data)

        db.session.add(topic)
        db.session.commit()

        return {"message": "Topic successfully created"}, 201

    # Function to edit an topic
    def put(self):
        contentful_data = request.get_json()
        topic = Topic.query.filter_by(contentful_id=contentful_data["entityId"]).first()
        edit_topic(topic, contentful_data)

        db.session.commit()

        return {"message": "Topic successfully updated"}, 200


# This class is used to delete an topic with a POST request
class TopicDelete(Resource):
    method_decorators = [topic_delete]

    # Function to delete a topic!!
    def post(self):
        contentful_data = request.get_json()
        topic = Topic.query.filter_by(contentful_id=contentful_data["entityId"]).first()
        delete_topic(topic)

        db.session.delete(topic)
        db.session.commit()

        return {"message": "Topic successfully deleted"}, 200


# Function to get a specific Topic based on topic id
class TopicGetSpecific(Resource):
    method_decorators = [topic_exists]

    def get(self, topic_id):
        topic = Topic.query.get(topic_id)

        return topic_schema.dump(topic)


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
        module_error = validate_module(module_id)

        if topic_error or module_error:
            return {
                       "message": "Topic or Module does not exist."
                   }, 500
        else:
            module = Module.query.get(module_id)

            if module not in student.incomplete_modules:
                return {
                           "message": "Module does not exist in the student's incomplete modules."
                       }, 500

            student.completed_modules.append(module)
            student.incomplete_modules.remove(module)
            db.session.commit()

        return {
                   "message": "Successfully updated student completed modules"
               }, 202


# Creates the routes for the classes
api.add_resource(TopicCRUD, "/topics")
api.add_resource(TopicDelete, "/topics/delete")
api.add_resource(TopicGetSpecific, "/topics/<int:topic_id>")
api.add_resource(TopicProgress, "/topics/<int:topic_id>/progress")
