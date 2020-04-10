from backend import safe_url
from backend.organizations.schemas import organization_file_schema, organization_form_schema
from backend.models import Organization, User
from flask import request, session
from flask_jwt_extended import get_jwt_identity
from functools import wraps


# Decorator to check if a user is in the organization
# This is used when sending invites to users to join an organization
def is_in_organization(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = safe_url.loads(kwargs["token"], salt="owner_invite", max_age=3600)
        email = data["email"]
        organization_id = data["organization_id"]
        user = User.query.filter_by(username=email).first()
        organization = Organization.query.get(organization_id)

        if not organization:
            return {
                       "message": "Organization does not exist"
                   }, 404

        if user not in organization.active_users or user not in organization.inactive_users:
            return {
                       "message": "The user does not belong in the organization. They have to join the organization first before becoming an owner."
                   }, 500
        return f(*args, **kwargs)
    return wrap


# Function to check if a user exists in an organization
def exist_in_organization(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        user = None
        data = request.get_json()

        if data:
            user = User.query.filter_by(username=data["username"]).first()
        else:
            username = get_jwt_identity()
            user = User.query.filter_by(username=username).first()
        organization = Organization.query.get(kwargs['organization_id'])

        if user in organization.active_users or user in organization.inactive_users:
            return f(*args, **kwargs)
        else:
            return {
                "message": "User does not belong in the organization"
            }, 500

    return wrap


# Function to check if a user has already joined the organization or not
# This is to prevent people from constantly rejoining
def has_joined_already(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        user_data = session["profile"]
        user = User.query.get(user_data["id"])
        organization = Organization.query.get(kwargs['organization_id'])

        if user in organization.active_users or user in organization.inactive_users:
            return {
                       "message": "You already joined the organization"
                   }, 500
        else:
            return f(*args, **kwargs)

    return wrap


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
        user_data = session["profile"]
        user = User.query.get(user_data["id"])
        organization = Organization.query.get(kwargs['organization_id'])

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
                   }, 422
        else:
            return f(*args, **kwargs)

    return wrap
