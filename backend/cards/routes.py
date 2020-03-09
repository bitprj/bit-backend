from flask import (Blueprint, request)
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from backend import api, db
from backend.authentication.decorators import roles_accepted
from backend.activity_progresses.utils import unlock_card
from backend.cards.decorators import card_exists, card_exists_in_activity, card_exists_in_github, card_is_unlockable, \
    valid_card_form
from backend.cards.schemas import card_schema
from backend.cards.utils import create_card, delete_card, edit_card
from backend.hints.schemas import hint_status_schemas
from backend.hints.utils import sort_hint_status
from backend.models import ActivityProgress, Card, Checkpoint, HintStatus, Student

# Blueprint for cards
cards_bp = Blueprint("cards", __name__)


# Class to Read, Create, and Update
class CardCRUD(Resource):

    # Function to create a card
    @valid_card_form
    def post(self):
        data = request.get_json()
        card = create_card(data)

        db.session.add(card)
        db.session.commit()

        return {"message": "Card successfully created"}, 201

    # Function to edit a card
    @valid_card_form
    @card_exists_in_github
    def put(self):
        data = request.get_json()
        card = Card.query.filter_by(github_raw_data=data["github_raw_data"]).first()
        edit_card(card, data)

        db.session.commit()

        return {"message": "Card successfully updated"}, 200

    # Function to delete a card
    @card_exists_in_github
    def delete(self):
        data = request.get_json()
        card = Card.query.filter_by(github_raw_data=data["github_raw_data"]).first()
        checkpoint = Checkpoint.query.filter_by(id=card.checkpoint.id).first()
        delete_card(card, checkpoint)

        db.session.delete(card)
        db.session.delete(checkpoint)
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
    method_decorators = [roles_accepted("Student"), card_exists, card_exists_in_activity]

    # Function to return data on the HintStatus
    def get(self, activity_id, card_id):
        username = get_jwt_identity()
        student = Student.query.filter_by(username=username).first()
        student_activity_prog = ActivityProgress.query.filter_by(student_id=student.id,
                                                                 activity_id=activity_id).first()
        hints = HintStatus.query.filter_by(activity_progress_id=student_activity_prog.id, card_id=card_id).all()
        sort_hint_status(hints)

        return hint_status_schemas.dump(hints)

    # Function to unlock the next card
    @card_is_unlockable
    def put(self, activity_id, card_id):
        username = get_jwt_identity()
        student = Student.query.filter_by(username=username).first()
        card = Card.query.get(card_id)
        student_activity_prog = ActivityProgress.query.filter_by(student_id=student.id,
                                                                 activity_id=activity_id).first()
        unlock_card(student_activity_prog, card)
        student_activity_prog.last_card_unlocked = card.id
        db.session.commit()

        return {
                   "message": "Card successfully updated"
               }, 202


# Creates the routes for the classes
api.add_resource(CardCRUD, "/cards")
api.add_resource(CardGetSpecific, "/cards/<int:card_id>")
api.add_resource(CardGetHints, "/activities/<int:activity_id>/cards/<int:card_id>")
