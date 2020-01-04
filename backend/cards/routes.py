from flask import (Blueprint, request)
from flask_restful import Resource
from backend import api, db
from backend.cards.schemas import card_schema
from backend.cards.utils import create_card, delete_card, edit_card
from backend.models import Card

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
        print(contentful_data)
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


# Creates the routes for the classes
api.add_resource(CardCRUD, "/cards")
api.add_resource(CardDelete, "/cards/delete")
api.add_resource(CardGetSpecific, "/cards/<int:card_id>")
