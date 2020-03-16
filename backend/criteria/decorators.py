from flask import request
from backend.criteria.schemas import criteria_form_schema
from backend.models import Criteria
from functools import wraps


# Decorator to check if a criteria exists in github
def criteria_exists_in_github(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        criteria = Criteria.query.filter_by(checkpoint_id=data["checkpoint_id"],
                                            criteria_key=data["criteria_key"]).first()

        if criteria:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Criteria does not exist"
                   }, 404

    return wrap


# Decorator to validate criteria form data
def valid_criteria_form(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.get_json()
        errors = criteria_form_schema.validate(data)

        if errors:
            return {
                       "message": "Missing or sending incorrect data to create a criteria. Double check the JSON data that it has everything needed to create a criteria."
                   }, 500
        else:
            return f(*args, **kwargs)

    return wrap
