from flask import request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims
from flask_praetorian.exceptions import MissingRoleError
from backend import guard
from backend.authentication.schemas import user_form_schema, user_login_schema
from backend.authentication.validators import check_user_existence
from functools import wraps


# Took inspiration from flask praetorian roles accepted decorator
# This is used to restrict a route to accept certain roles
def roles_accepted(*accepted_rolenames):
    def decorator(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            role_set = set([str(n) for n in accepted_rolenames])
            verify_jwt_in_request()
            claims = get_jwt_claims()
            user_roles = set(r.strip() for r in claims['roles'].split(','))

            try:
                MissingRoleError.require_condition(
                    not user_roles.isdisjoint(role_set),
                    "This endpoint requires one of the following roles: {}",
                    [', '.join(role_set)],
                )
                return method(*args, **kwargs)
            finally:
                print("Role requirement complete")
        return wrapper
    return decorator


# Took inspiration from flask praetorian roles required decorator
# This is used to restrict routes to user roles
def roles_required(*required_rolenames):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            role_set = set([str(n) for n in required_rolenames])
            verify_jwt_in_request()
            claims = get_jwt_claims()
            user_roles = set(r.strip() for r in claims['roles'].split(','))

            try:
                MissingRoleError.require_condition(
                    user_roles.issuperset(role_set),
                    "This endpoint requires all the following roles: {}",
                    [', '.join(role_set)],
                )
                return f(*args, **kwargs)
            finally:
                print("Role requirement complete")
        return wrapper
    return decorator


# Decorator to check if the user is logged in
def user_exists(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        form_data = request.get_json()
        errors = user_login_schema.validate(form_data)

        # If form data is not validated by the user_form_schema, then return a 500 error
        # else proceed to check if the user exists
        if errors:
            return {
                       "message": "Missing or sending incorrect login data. Double check the JSON data that it has everything needed to login."
                   }, 500
        else:
            username = form_data["username"]
            password = form_data["password"]
            user = guard.authenticate(username, password)

            if user:
                return f(*args, **kwargs)
            else:
                return {
                           "message": "User does not exist"
                       }, 404

    return wrap


# Decorator to check if a user registration data is valid
def valid_user_form(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        form_data = request.get_json()
        errors = user_form_schema.validate(form_data)

        if errors:
            return {
                       "message": "Missing or sending incorrect data to create a " + kwargs[
                           "user_type"] + ". Double check the JSON data that it has everything needed to create a " + user_type + "."
                   }, 500
        else:
            user_already_exist = check_user_existence(form_data["username"])

            # If user exist in the database, then return an error message to
            # tell the user to choose a different email
            if user_already_exist:
                return {
                           "message": "Email already exists. Please choose another one."
                       }, 500
            else:
                return f(*args, **kwargs)

    return wrap
