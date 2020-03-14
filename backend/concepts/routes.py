from flask import (Blueprint, request)
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from backend import api, db
from backend.concepts.decorators import concept_exists, concept_exists_in_github, valid_concept_form
from backend.concepts.schemas import concept_schema
from backend.concepts.utils import create_concept, edit_concept
from backend.hooks.utils import call_step_routes, delete_step_route
from backend.models import Concept

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
        call_step_routes(data["steps"], concept.id, "concept", data["image_folder"])
        db.session.commit()

        return {"message": "Concept successfully created"}, 201

    # Function to edit an concept
    @valid_concept_form
    @concept_exists_in_github
    def put(self):
        data = request.get_json()
        concept = Concept.query.filter_by(filename=data["filename"]).first()
        delete_step_route(concept.steps)
        edit_concept(concept, data)
        call_step_routes(data["steps"], concept.id, "concept", data["image_folder"])

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
    method_decorators = [jwt_required, concept_exists]

    def get(self, concept_id):
        concept = Concept.query.get(concept_id)

        return concept_schema.dump(concept)


# Creates the routes for the classes
api.add_resource(ConceptCRUD, "/concepts")
api.add_resource(ConceptGetSpecific, "/concepts/<int:concept_id>")
