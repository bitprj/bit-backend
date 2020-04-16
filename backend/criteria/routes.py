from backend import api, db
from backend.criteria.decorators import criteria_exists_in_github, valid_criteria_form
from backend.criteria.utils import create_criteria, edit_criteria
from backend.models import Criteria
from flask import Blueprint, request
from flask_restful import Resource


# Blueprint for criteria
criteria_bp = Blueprint("criteria", __name__)


# Class to Read, Create, and Update
class CriteriaCRUD(Resource):

    # Function to create a criteria
    @valid_criteria_form
    def post(self):
        data = request.get_json()
        criteria = create_criteria(data)

        db.session.add(criteria)
        db.session.commit()

        return {"message": "Criteria successfully created"}, 201

    # Function to edit a criteria
    @valid_criteria_form
    @criteria_exists_in_github
    def put(self):
        data = request.get_json()
        criteria = Criteria.query.filter_by(checkpoint_id=data["checkpoint_id"],
                                            criteria_key=data["criteria_key"]).first()
        edit_criteria(criteria, data)

        db.session.commit()

        return {"message": "Criteria successfully updated"}, 200

    # Function to delete a criteria
    @criteria_exists_in_github
    def delete(self):
        data = request.get_json()
        criteria = Criteria.query.filter_by(checkpoint_id=data["checkpoint_id"],
                                            criteria_key=data["criteria_key"]).first()

        db.session.delete(criteria)
        db.session.commit()

        return {"message": "Criteria successfully deleted"}, 200


# Creates the routes for the classes
api.add_resource(CriteriaCRUD, "/criteria")
