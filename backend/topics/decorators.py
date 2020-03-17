from flask import request
from flask_jwt_extended import get_jwt_identity
from backend.models import Student, Topic
from backend.topics.schemas import topic_form_schema
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


# Decorator to check if a topic exists in github
def topic_exists_in_github(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        topic = Topic.query.filter_by(filename=data["filename"]).first()

        if topic:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Topic does not exist"
                   }, 404

    return wrap


# Decorator to check if a topic is in the incomplete column
def topic_is_incomplete(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        username = get_jwt_identity()
        student = Student.query.filter_by(username=username).first()
        topic = Topic.query.get(kwargs["topic_id"])

        if topic in student.incomplete_topics:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Topic has already been added!"
                   }, 500

    return wrap


# Decorator to validate topic form data
def valid_topic_form(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        errors = topic_form_schema.validate(data)

        if errors:
            return {
                       "message": "Missing or sending incorrect data to create a topic. Double check the JSON data that it has everything needed to create a topic."
                   }, 500
        else:
            return f(*args, **kwargs)

    return wrap
