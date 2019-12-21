from flask import (Blueprint, request)
from flask_restful import Resource
from backend import api, db
from backend.models import Concept
from backend.prereqs.validators import validate_cards
from backend.concepts.schemas import concept_schema, concept_form_schema
from backend.concepts.utils import create_concept, edit_concept
from backend.steps.utils import validate_step_data

# Blueprint for concepts
concepts_bp = Blueprint("concepts", __name__)


# Class to Read, Update, and Destroy routes
class ConceptData(Resource):
    # Function to return data on a single concept
    def get(self, concept_id):
        concept = Concept.query.get(concept_id)

        # If concept does not exists, then return a 404 error
        # else return the concept back to the user
        if not concept:
            return {"message": "Concept does not exist"}, 404
        else:
            return concept_schema.dump(concept)

    # Function to edit a concept
    def put(self, concept_id):
        concept = Concept.query.get(concept_id)

        # If concept does not exist, then return a 404 error
        # else edit a concept and edit it in the database
        if not concept:
            return {"message": "Concept does not exist"}, 404
        else:
            form_data = request.get_json()
            errors = concept_form_schema.validate(form_data)
            step_error = validate_step_data(form_data["steps"])

            # If form data is not validated by the concept_schema, then return a 500 error
            # else edit the concept and save it to the database
            if errors or step_error:
                return {
                           "message": "Missing or sending incorrect data to edit a concept. Double check the JSON data that it has everything needed to edit a concept."
                       }, 500
            else:
                edit_concept(concept, form_data)
                db.session.commit()

            return {"message": "Concept successfully updated"}, 202

    # Function to delete a concept
    def delete(self, concept_id):
        concept = Concept.query.get(concept_id)

        # If concept does not exists, return a 404 error
        # else delete the concept and save to database
        if not concept:
            return {"message": "Concept does not exists"}, 404
        else:
            db.session.delete(concept)
            db.session.commit()

        return {"message": "Concept successfully deleted"}, 200


# Class to define concept creation
class ConceptCreate(Resource):
    # Function to create a concept
    def post(self):
        form_data = request.get_json()
        errors = concept_form_schema.validate(form_data)
        step_error = validate_step_data(form_data["steps"])

        # If form data is not validated by the concept_schema, then return a 500 error
        # else create the concept and add it to the database
        if errors or step_error:
            return {
                       "message": "Missing or sending incorrect data to create a concept. Double check the JSON data that it has everything needed to create a concept."
                   }, 500
        else:
            card_error = validate_cards(form_data["cards"])

            if card_error:
                return {
                           "message": "Card does not exist. Double check the arrays to check if they are valid in the database."
                       }, 500
            else:
                concept = create_concept(form_data)
                db.session.add(concept)
                db.session.commit()

        return {"message": "Concept successfully created"}, 202


# Creates the routes for the classes
api.add_resource(ConceptData, "/concepts/<int:concept_id>")
api.add_resource(ConceptCreate, "/concepts/create")
