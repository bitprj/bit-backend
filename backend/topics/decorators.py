from flask import request
from backend import contentful_client
from backend.config import SPACE_ID
from backend.models import Topic
from functools import wraps


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
