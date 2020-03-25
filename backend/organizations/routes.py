from flask import (Blueprint, request, session)
from flask_restful import Resource
from backend import api, db, safe_url
from backend.authentication.decorators import auth0_auth
from backend.organizations.decorators import is_in_organization, exist_in_organization, has_joined_already, \
    organization_exists, owns_organization, valid_organization_form
from backend.organizations.schemas import organization_schema
from backend.organizations.utils import create_organization, edit_organization, remove_user, send_invites
from backend.models import Organization, User
from itsdangerous import SignatureExpired

# Blueprint for organizations
organizations_bp = Blueprint("organizations", __name__)


# Class for organization CRUD routes
class OrganizationCRUD(Resource):
    method_decorators = [auth0_auth, organization_exists]

    def get(self, organization_id):
        organization = Organization.query.get(organization_id)

        return organization_schema.dump(organization)

    # Function to edit a organization
    @owns_organization
    @valid_organization_form
    def put(self, organization_id):
        organization = Organization.query.get(organization_id)
        form_data = request.form
        form_files = request.files
        edit_organization(organization, form_data, form_files)

        db.session.commit()

        return {"message": "Organization successfully updated"}, 202

    # Function to delete a organization!!
    @owns_organization
    def delete(self, organization_id):
        organization = Organization.query.get(organization_id)

        db.session.delete(organization)
        db.session.commit()

        return {"message": "Organization successfully deleted"}, 200


# This class is used to delete an organization with a POST request
class OrganizationCreate(Resource):
    method_decorators = [auth0_auth, valid_organization_form]

    # Function to create a organization
    def post(self):
        form_data = request.form
        form_files = request.files
        username = session["username"]
        user = User.query.filter_by(username=username).first()
        organization = create_organization(form_data, form_files, user)

        db.session.add(organization)
        db.session.commit()

        return {"message": "Organization successfully created"}, 202


class OrganizationInviteConfirm(Resource):
    method_decorators = [is_in_organization]

    # Route to add a person to be an owner of an organization
    def get(self, token):
        email = None
        organization_id = None

        try:
            data = safe_url.loads(token, salt="owner_invite", max_age=3600)
            email = data["email"]
            organization_id = data["organization_id"]
        except SignatureExpired:
            return {
                       "message": "Your invitation has expired."
                   }, 500

        user = User.query.filter_by(username=email).first()
        organization = Organization.query.get(organization_id)
        organization.owners.append(user)
        db.session.commit()
        # TODO replace this to redirect to Bryan Z's frontend route
        return {
                   "message": "Your are now an owner of the organization"
               }, 200


# This class allows owners of an organization to invite
# other people to be owners of their organization
class OrganizationInviteOwners(Resource):
    method_decorators = [auth0_auth, organization_exists]

    # Function to invite other users to be owners of an organization
    @owns_organization
    def put(self, organization_id):
        data = request.get_json()
        organization = Organization.query.get(organization_id)
        send_invites(data["people"], organization)

        return {
                   "message": "Invites have been sent"
               }, 200


# This class is used to allow people to join an organization
class OrganizationMembership(Resource):
    method_decorators = [auth0_auth, organization_exists]

    # Function to let a user join an organization
    @has_joined_already
    def put(self, organization_id):
        username = session["username"]
        user = User.query.filter_by(username=username).first()
        organization = Organization.query.get(organization_id)
        organization.active_users.append(user)
        db.session.commit()

        return {
                   "message": user.name + " has joined " + organization.name
               }, 200

    # Function to let a user leave an organization
    @exist_in_organization
    def delete(self, organization_id):
        username = session["username"]
        user = User.query.filter_by(username=username).first()
        organization = Organization.query.get(organization_id)
        remove_user(organization, user)
        db.session.commit()

        return {
                   "message": "You successfully left " + organization.name
               }, 200


# This class is used to allow owners of an organization to kick people out of their organization
class OrganizationRemove(Resource):
    method_decorators = [auth0_auth, organization_exists]

    # Function to remove a user from an organization
    # Only owners can kick people out
    @owns_organization
    @exist_in_organization
    def delete(self, organization_id):
        data = request.get_json()
        username = data["username"]
        user = User.query.filter_by(username=username).first()
        organization = Organization.query.get(organization_id)
        remove_user(organization, user)

        db.session.commit()

        return {
                   "message": "Removed " + user.name + " from " + organization.name
               }, 200


# Creates the routes for the classes
api.add_resource(OrganizationCRUD, "/organizations/<int:organization_id>")
api.add_resource(OrganizationCreate, "/organizations/create")
api.add_resource(OrganizationInviteOwners, "/organizations/<int:organization_id>/invite")
api.add_resource(OrganizationInviteConfirm, "/organizations/<string:token>")
api.add_resource(OrganizationMembership, "/organizations/<int:organization_id>/membership")
api.add_resource(OrganizationRemove, "/organizations/<int:organization_id>/remove")
