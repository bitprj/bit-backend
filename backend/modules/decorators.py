from flask import request
from backend import contentful_client
from backend.config import SPACE_ID
from backend.models import Module
from functools import wraps


# Decorator to check if a module exists
def module_exists(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        module = Module.query.get(kwargs['module_id'])

        if module:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Module does not exist"
                   }, 404

    return wrap


# Decorator to check if a module exists in contentful
def module_exists_in_contentful(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        content_type = data["contentType"]["sys"]["id"]
        module = Module.query.filter_by(contentful_id=data["entityId"]).first()
        contentful_module = contentful_client.entries(SPACE_ID, 'master').find(data["entityId"])
        # Checks if the module exists in contentful and if its a module
        # Checks if the module exists in the db for put request
        if contentful_module and content_type == "module" or module:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Module does not exist"
                   }, 404

    return wrap


# Decorator to check if the module can be deleted
def module_delete(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        module = Module.query.filter_by(contentful_id=data["entityId"]).first()

        if module:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Module does not exist"
                   }, 404

    return wrap
