from flask import (Blueprint, request)
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from backend import api, db
from backend.mc_questions.decorators import mc_question_delete, mc_question_exists, mc_question_exists_in_contentful
from backend.mc_questions.schemas import mc_question_schema
from backend.mc_questions.utils import create_mc_question, edit_mc_question
from backend.models import MCQuestion

# Blueprint for mc_questions
mc_questions_bp = Blueprint("mc_questions", __name__)


# Class to Read, Create, and Update
class MCQuestionCRUD(Resource):

    # Function to create a mc_question
    def post(self):
        contentful_data = request.get_json()
        mc_question = create_mc_question(contentful_data)

        db.session.add(mc_question)
        db.session.commit()

        return {"message": "MCQuestion successfully created"}, 201

    # Function to edit a mc_question
    @mc_question_exists_in_contentful
    def put(self):
        contentful_data = request.get_json()
        mc_question = MCQuestion.query.filter_by(contentful_id=contentful_data["entityId"]).first()
        edit_mc_question(mc_question, contentful_data)

        db.session.commit()

        return {"message": "MCQuestion successfully updated"}, 200


# This class is used to delete a mc_question with a POST request
class MCQuestionDelete(Resource):
    method_decorators = [mc_question_delete]

    # Function to delete a mc_question
    def post(self):
        contentful_data = request.get_json()
        mc_question = MCQuestion.query.filter_by(contentful_id=contentful_data["entityId"]).first()

        db.session.delete(mc_question)
        db.session.commit()

        return {"message": "MCQuestion successfully deleted"}, 200


# This class is used to get a specific mc_question based on id
class MCQuestionGetSpecific(Resource):
    method_decorators = [jwt_required, mc_question_exists]

    # Function to return data on a single mc_question
    def get(self, mc_question_id):
        mc_question = MCQuestion.query.get(mc_question_id)

        return mc_question_schema.dump(mc_question)


# Creates the routes for the classes
api.add_resource(MCQuestionCRUD, "/mc_questions")
api.add_resource(MCQuestionDelete, "/mc_questions/delete")
api.add_resource(MCQuestionGetSpecific, "/mc_questions/<int:mc_question_id>")
