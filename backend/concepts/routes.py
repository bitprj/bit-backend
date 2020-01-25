from flask import (Blueprint, request)
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from backend import api, db
from backend.concepts.decorators import concept_delete, concept_exists, concept_exists_in_contentful
from backend.concepts.schemas import concept_schema
from backend.concepts.utils import create_concept, delete_concept, edit_concept
from backend.models import Concept

# Blueprint for concepts
concepts_bp = Blueprint("concepts", __name__)


# Class for concept CRUD routes
class ConceptCRUD(Resource):

    # Function to create a concept
    def post(self):
        contentful_data = request.get_json()
        concept = create_concept(contentful_data)

        db.session.add(concept)
        db.session.commit()

        return {"message": "Concept successfully created"}, 201

    # Function to edit an concept
    @concept_exists_in_contentful
    def put(self):
        contentful_data = request.get_json()
        concept = Concept.query.filter_by(contentful_id=contentful_data["entityId"]).first()
        edit_concept(concept, contentful_data)

        db.session.commit()

        return {"message": "Concept successfully updated"}, 200


# This class is used to delete an concept with a POST request
class ConceptDelete(Resource):
    method_decorators = [concept_delete]

    # Function to delete a concept!!
    def post(self):
        contentful_data = request.get_json()
        concept = Concept.query.filter_by(contentful_id=contentful_data["entityId"]).first()
        delete_concept(concept)

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
api.add_resource(ConceptDelete, "/concepts/delete")
api.add_resource(ConceptGetSpecific, "/concepts/<int:concept_id>")
