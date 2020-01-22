from flask import (Blueprint, request)
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from backend import api, db
from backend.authentication.decorators import roles_accepted
from backend.activity_progresses.utils import unlock_card
from backend.cards.decorators import card_delete, card_exists, card_exists_in_contentful
from backend.cards.schemas import card_schema
from backend.cards.utils import create_card, delete_card, edit_card
from backend.hints.schemas import hint_status_schemas
from backend.models import ActivityProgress, Card, Student

# Blueprint for cards
cards_bp = Blueprint("cards", __name__)


# Class to Read, Create, and Update
class CardCRUD(Resource):
    method_decorators = [card_exists_in_contentful]

    # Function to create a card
    def post(self):
        contentful_data = request.get_json()
        card = create_card(contentful_data)

        db.session.add(card)
        db.session.commit()
        print(card.id)

        return {"message": "Card successfully created"}, 201

    # Function to edit a card
    def put(self):
        contentful_data = request.get_json()
        card = Card.query.filter_by(contentful_id=contentful_data["entityId"]).first()
        edit_card(card, contentful_data)

        db.session.commit()

        return {"message": "Card successfully updated"}, 200


# This class is used to delete a card with a POST request
class CardDelete(Resource):
    method_decorators = [card_delete]

    # Function to delete a card
    def post(self):
        contentful_data = request.get_json()
        card = Card.query.filter_by(contentful_id=contentful_data["entityId"]).first()
        delete_card(card)

        db.session.delete(card)
        db.session.commit()

        return {"message": "Card successfully deleted"}, 200


# This class is used to get a specific card based on id
class CardGetSpecific(Resource):
    method_decorators = [jwt_required, card_exists]

    # Function to return data on a single card
    def get(self, card_id):
        card = Card.query.get(card_id)

        return card_schema.dump(card)


# This class is used to return data on the locked and unlocked hints for a card on a user
class CardGetHints(Resource):
    method_decorators = [roles_accepted("Student"), card_exists]

    # Function to return data on a single card
    def get(self, activity_id, card_id):
        username = get_jwt_identity()
        student = Student.query.filter_by(username=username).first()
        card = Card.query.get(card_id)

        student_activity_prog = ActivityProgress.query.filter_by(student_id=student.id,
                                                                 activity_id=activity_id).first()
        if card in student_activity_prog.activity.cards:
            if card in student_activity_prog.cards_locked:
                unlock_card(student_activity_prog, card)
                db.session.commit()

            student_activity_prog.lawhst_card_completed = card.id

            return hint_status_schemas.dump(student_activity_prog.hints)
        return {
                   "message": "Card does not belong in activity"
               }, 500


# Creates the routes for the classes
api.add_resource(CardCRUD, "/cards")
api.add_resource(CardDelete, "/cards/delete")
api.add_resource(CardGetSpecific, "/cards/<int:card_id>")
api.add_resource(CardGetHints, "/activities/<int:activity_id>/cards/<int:card_id>/fetch")
