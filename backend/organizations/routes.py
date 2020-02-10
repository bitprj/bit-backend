from flask import (Blueprint, request)
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from backend import api, db
from backend.authentication.decorators import roles_accepted
from backend.organizations.decorators import organization_exists, owns_organization, valid_organization_form
from backend.organizations.schemas import organization_schema
from backend.organizations.utils import create_organization, edit_organization
from backend.models import Organization, User

# Blueprint for organizations
organizations_bp = Blueprint("organizations", __name__)


# Class for organization CRUD routes
class OrganizationCRUD(Resource):
    method_decorators = [jwt_required, organization_exists]

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
    method_decorators = [jwt_required, valid_organization_form]

    # Function to create a organization
    def post(self):
        form_data = request.form
        form_files = request.files
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        organization = create_organization(form_data, form_files, user)

        db.session.add(organization)
        db.session.commit()

        return {"message": "Organization successfully created"}, 202


# Creates the routes for the classes
api.add_resource(OrganizationCRUD, "/organizations/<int:organization_id>")
api.add_resource(OrganizationCreate, "/organizations/create")
