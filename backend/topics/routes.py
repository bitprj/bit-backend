from flask import (Blueprint, request)
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from backend import api, db
from backend.models import Topic
from backend.topics.decorators import topic_delete, topic_exists, topic_exists_in_contentful
from backend.topics.schemas import topic_schema
from backend.topics.utils import create_topic, delete_topic, edit_topic

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
    method_decorators = [jwt_required, topic_exists]

    def get(self, topic_id):
        topic = Topic.query.get(topic_id)

        return topic_schema.dump(topic)


# Creates the routes for the classes
api.add_resource(TopicCRUD, "/topics")
api.add_resource(TopicDelete, "/topics/delete")
api.add_resource(TopicGetSpecific, "/topics/<int:topic_id>")
