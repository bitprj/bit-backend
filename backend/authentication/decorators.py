from backend.authentication.schemas import valid_access_token
from backend.general_utils import verify_user_session
from flask import request, session
from flask_praetorian.exceptions import MissingRoleError
from functools import wraps


# Decorator to check if the access token exists in the Github Callback
def access_token_exists(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = {"code": request.args.get("code")}
        errors = valid_access_token.validate(data)

        if errors:
            return {
                       "message": "Invalid access token"
                   }, 422
        else:
            return f(*args, **kwargs)

    return wrap


# Took inspiration from flask praetorian roles accepted decorator
# This is used to restrict a route to accept certain roles
def roles_accepted(*accepted_rolenames):
    def decorator(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            verify_user_session()
            role_set = set([str(n) for n in accepted_rolenames])
            user_roles = set(r.strip() for r in session["profile"]["roles"].split(','))

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
            verify_user_session()
            role_set = set([str(n) for n in required_rolenames])
            user_roles = set(r.strip() for r in session["profile"]["roles"].split(','))

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
def user_session_exists(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        print(session["profile"])
        if "profile" in session:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "User is not logged in"
                   }, 401

    return wrap
