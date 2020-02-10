from flask import request
from flask_jwt_extended import get_jwt_identity
from backend.organizations.schemas import organization_file_schema, organization_form_schema
from backend.models import Organization, User
from functools import wraps


# Decorator to check if a organization exists
def organization_exists(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        organization = Organization.query.get(kwargs['organization_id'])

        if organization:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Organization does not exist"
                   }, 404

    return wrap


# Decorator to check if a teacher owns a organizations
def owns_organization(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        organization = Organization.query.get(kwargs['organization_id'])
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()

        if user in organization.owners:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "You do not own this organization"
                   }, 203

    return wrap


# Decorator to check if a organization form data is valid
def valid_organization_form(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        errors = organization_form_schema.validate(request.form)
        errors_2 = organization_file_schema.validate(request.files)

        # If form data is not validated by the organization_schema, then return a 500 error
        # else create the organization and add it to the database
        if errors or errors_2:
            return {
                       "message": "Missing or sending incorrect data to create a organization. Double check the JSON data that it has everything needed to create a organization."
                   }, 500
        else:
            return f(*args, **kwargs)

    return wrap
