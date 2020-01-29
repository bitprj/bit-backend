from flask import request
from flask_jwt_extended import get_jwt_identity
from backend import contentful_client
from backend.config import SPACE_ID
from backend.models import Student, Topic
from backend.topics.utils import completed_modules
from functools import wraps


# Decorator to check if a student is allowed to access a module or not
def can_add_topic(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        username = get_jwt_identity()
        student = Student.query.filter_by(username=username).first()
        topic = Topic.query.get(kwargs['topic_id'])
        can_add = completed_modules(student, topic.module_prereqs)

        if can_add:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "You have not completed the prerequisites for this topic"
                   }, 500

    return wrap


# Decorator to check if a student is allowed to complete a topic
def can_complete_topic(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        username = get_jwt_identity()
        student = Student.query.filter_by(username=username).first()
        topic = Topic.query.get(kwargs['topic_id'])
        can_complete = completed_modules(student, topic.modules)

        if can_complete:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "You have not completed enough modules to pass the topic"
                   }, 500

    return wrap


# Decorator to check if a student has already completed a topic
def has_completed_topic(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        username = get_jwt_identity()
        student = Student.query.filter_by(username=username).first()
        topic = Topic.query.get(kwargs['topic_id'])

        if topic in student.completed_topics and topic not in student.inprogress_topics:
            return {
                       "message": "Topic already completed"
                   }, 500

        return f(*args, **kwargs)

    return wrap


# Decorator to check if a topic exists
def topic_exists(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        topic = Topic.query.get(kwargs['topic_id'])

        if topic:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Topic does not exist"
                   }, 404

    return wrap


# Decorator to check if a topic exists in contentful
def topic_exists_in_contentful(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        content_type = data["contentType"]["sys"]["id"]
        topic = Topic.query.filter_by(contentful_id=data["entityId"]).first()
        contentful_topic = contentful_client.entries(SPACE_ID, 'master').find(data["entityId"])

        # Checks if the topic exists in contentful and if its a topic
        # Checks if the topic exists in the db for put request
        if contentful_topic and content_type == "topic" or topic:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Topic does not exist"
                   }, 404

    return wrap


# Decorator to check if the topic can be deleted
def topic_delete(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        topic = Topic.query.filter_by(contentful_id=data["entityId"]).first()

        if topic:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Topic does not exist"
                   }, 404

    return wrap
