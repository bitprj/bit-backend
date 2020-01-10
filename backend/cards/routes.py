from flask import (Blueprint, request)
from flask_praetorian import roles_accepted
from flask_restful import Resource
from backend import api, db
from backend.activity_progresses.utils import unlock_card
from backend.cards.schemas import card_schema
from backend.cards.utils import create_card, delete_card, edit_card
from backend.general_utils import get_user_id_from_token
from backend.hints.schemas import hint_status_schemas
from backend.models import ActivityProgress, Card

# Blueprint for cards
cards_bp = Blueprint("cards", __name__)


# Class to Read, Create, and Update
class CardCRUD(Resource):
    # Function to create a card
    def post(self):
        contentful_data = request.get_json()
        card = create_card(contentful_data)

        db.session.add(card)
        db.session.commit()

        return {"message": "Card successfully created"}, 201

    # Function to edit a card
    def put(self):
        contentful_data = request.get_json()
        card = Card.query.filter_by(contentful_id=contentful_data["entityId"]).first()

        if not card:
            return {"message": "Card does not exist"}, 404

        edit_card(card, contentful_data)

        db.session.commit()

        return {"message": "Card successfully updated"}, 200


# This class is used to delete a card with a POST request
class CardDelete(Resource):
    # Function to delete a card
    def post(self):
        contentful_data = request.get_json()
        card = Card.query.filter_by(contentful_id=contentful_data["entityId"]).first()

        if not card:
            return {"message": "Card does not exist"}, 404

        delete_card(card)

        db.session.delete(card)
        db.session.commit()

        return {"message": "Card successfully deleted"}, 200


# This class is used to get a specific card based on id
class CardGetSpecific(Resource):
    # Function to return data on a single card
    def get(self, card_id):
        card = Card.query.get(card_id)

        # If card does not exists, then return a 404 error
        # else return the card back to the user
        if not card:
            return {"message": "Card does not exist"}, 404
        else:
            return card_schema.dump(card)


# This class is used to return data on the locked and unlocked hints for a card on a user
class CardGetHints(Resource):
    method_decorators = [roles_accepted("Student")]

    # Function to return data on a single card
    def get(self, activity_id, card_id):
        current_user_id = get_user_id_from_token()
        card = Card.query.get(card_id)

        # If card does not exists, then return a 404 error
        # else return the card back to the user
        if not card:
            return {"message": "Card does not exist"}, 404
        else:
            student_activity_prog = ActivityProgress.query.filter_by(student_id=current_user_id,
                                                                     activity_id=activity_id).first()
            if card in student_activity_prog.activity.cards:
                if card in student_activity_prog.cards_locked:
                    unlock_card(student_activity_prog, card)
                    db.session.commit()

                student_activity_prog.last_card_completed = card.id

                return hint_status_schemas.dump(student_activity_prog.hints)
            return {
                       "message": "Card does not belong in activity"
                   }, 500


# Creates the routes for the classes
api.add_resource(CardCRUD, "/cards")
api.add_resource(CardDelete, "/cards/delete")
api.add_resource(CardGetSpecific, "/cards/<int:card_id>")
api.add_resource(CardGetHints, "/activities/<int:activity_id>/cards/<int:card_id>/fetch")
