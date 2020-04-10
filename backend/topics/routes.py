from backend import api, db
from backend.authentication.decorators import user_session_exists
from backend.general_utils import create_schema_json
from backend.models import Topic
from backend.topics.decorators import topic_exists, topic_exists_in_github, valid_topic_form
from backend.topics.schemas import topic_schema
from backend.topics.utils import create_topic, delete_topic, edit_topic
from flask import Blueprint, request
from flask_restful import Resource

# Blueprint for topics
topics_bp = Blueprint("topics", __name__)


# Class for topic CRUD routes
class TopicCRUD(Resource):
    # Function to create a topic
    @valid_topic_form
    def post(self):
        data = request.get_json()
        topic = create_topic(data)

        db.session.add(topic)
        db.session.commit()
        create_schema_json(topic, "topics")
        db.session.commit()

        return {"message": "Topic successfully created"}, 201

    # Function to edit an topic
    @topic_exists_in_github
    @valid_topic_form
    def put(self):
        data = request.get_json()
        topic = Topic.query.filter_by(filename=data["filename"]).first()
        edit_topic(topic, data)

        db.session.commit()

        return {"message": "Topic successfully updated"}, 200

    # Function to delete a topic!!
    @topic_exists_in_github
    def delete(self):
        data = request.get_json()
        topic = Topic.query.filter_by(filename=data["filename"]).first()
        delete_topic(topic)

        db.session.delete(topic)
        db.session.commit()

        return {"message": "Topic successfully deleted"}, 200


# Function to get a specific Topic based on topic id
class TopicGetSpecific(Resource):
    method_decorators = [user_session_exists, topic_exists]

    def get(self, topic_id):
        topic = Topic.query.get(topic_id)

        return topic_schema.dump(topic)


# Creates the routes for the classes
api.add_resource(TopicCRUD, "/topics")
api.add_resource(TopicGetSpecific, "/topics/<int:topic_id>")
