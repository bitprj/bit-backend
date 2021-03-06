from backend import api, db
from backend.authentication.decorators import user_session_exists
from backend.concepts.decorators import concept_exists, concept_exists_in_github, valid_concept_form
from backend.concepts.schemas import concept_schema
from backend.concepts.utils import create_concept, edit_concept
from backend.general_utils import create_schema_json
from backend.hooks.utils import call_step_routes
from backend.models import Concept
from flask import Blueprint, request
from flask_restful import Resource


# Blueprint for concepts
concepts_bp = Blueprint("concepts", __name__)


# Class for concept CRUD routes
class ConceptCRUD(Resource):

    # Function to create a concept
    @valid_concept_form
    def post(self):
        data = request.get_json()
        concept = create_concept(data)

        db.session.add(concept)
        db.session.commit()
        call_step_routes(data, concept.id, "concept")
        create_schema_json(concept, "concepts")
        db.session.commit()

        return {"message": "Concept successfully created"}, 201

    # Function to edit an concept
    @valid_concept_form
    @concept_exists_in_github
    def put(self):
        data = request.get_json()
        concept = Concept.query.filter_by(filename=data["filename"]).first()
        edit_concept(concept, data)

        db.session.commit()

        return {"message": "Concept successfully updated"}, 200

    # Function to delete a concept!!
    @concept_exists_in_github
    def delete(self):
        data = request.get_json()
        concept = Concept.query.filter_by(filename=data["filename"]).first()

        db.session.delete(concept)
        db.session.commit()

        return {"message": "Concept successfully deleted"}, 200


# Function to get a specific Concept based on concept id
class ConceptGetSpecific(Resource):
    method_decorators = [user_session_exists, concept_exists]

    def get(self, concept_id):
        concept = Concept.query.get(concept_id)

        return concept_schema.dump(concept)


# Creates the routes for the classes
api.add_resource(ConceptCRUD, "/concepts")
api.add_resource(ConceptGetSpecific, "/concepts/<int:concept_id>")
