from flask import (Blueprint, request)
from flask_restful import Resource
from backend import api, db
from backend.models import Concept
from backend.concepts.schemas import concept_schema
from backend.concepts.utils import create_concept, edit_concept

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
    def put(self):
        contentful_data = request.get_json()
        concept = Concept.query.filter_by(contentful_id=contentful_data["entityId"]).first()
        edit_concept(concept, contentful_data)

        db.session.commit()

        return {"message": "Concept successfully updated"}, 200


# Function to get a specific Concept based on concept id
class ConceptGetSpecific(Resource):
    def get(self, concept_id):
        concept = Concept.query.get(concept_id)

        if not concept:
            return {"message": "Concept does not exist"}, 404

        return concept_schema.dump(concept)


# This class is used to delete an concept with a POST request
class ConceptDelete(Resource):
    # Function to delete a concept!!
    def post(self):
        contentful_data = request.get_json()
        concept = Concept.query.filter_by(contentful_id=contentful_data["entityId"]).first()

        if not concept:
            return {"message": "Concept does not exist"}, 404

        db.session.delete(concept)
        db.session.commit()

        return {"message": "Concept successfully deleted"}, 200


# Creates the routes for the classes
api.add_resource(ConceptCRUD, "/concepts")
api.add_resource(ConceptDelete, "/concepts/delete")
api.add_resource(ConceptGetSpecific, "/concepts/<int:concept_id>")
