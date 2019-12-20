from flask import (Blueprint, request)
from flask_restful import Resource
from backend import api, db
from backend.models import Card


# Blueprint for cards
cards_bp = Blueprint("cards", __name__)


# Class to Read, Update, and Destroy routes
class CardData(Resource):
    # Function to return data on a single card
    def get(self, card_id):
        card = Card.query.get(card_id)

        # If card does not exists, then return a 404 error
        # else return the card back to the user
        if not card:
            return {"message": "Card does not exist"}, 404
        else:
            return card_schema.dump(card)

    # Function to edit a card
    def put(self, card_id):
        card = Card.query.get(card_id)

        # If card does not exist, then return a 404 error
        # else edit a card and edit it in the database
        if not card:
            return {"message": "Card does not exist"}, 404
        else:
            form_data = request.get_json()
            errors = card_form_schema.validate(form_data)

            # If form data is not validated by the card_schema, then return a 500 error
            # else edit the card and save it to the database
            if errors:
                return {
                            "message": "Missing or sending incorrect data to edit a card. Double check the JSON data that it has everything needed to edit a card."
                       }, 500
            else:
                edit_card(card, form_data)
                db.session.commit()

            return {"message": "Card successfully updated"}, 202

    # Function to delete a card
    def delete(self, card_id):
        card = Card.query.get(card_id)

        # If card does not exists, return a 404 error
        # else delete the card and save to database
        if not card:
            return {"message": "Card does not exists"}, 404
        else:
            db.session.delete(card)
            db.session.commit()

        return {"message": "Card successfully deleted"}, 200


# Class to define card creation
class CardCreate(Resource):
    # Function to create a card
    def post(self):
        form_data = request.get_json()
        errors = card_form_schema.validate(form_data)

        # If form data is not validated by the card_schema, then return a 500 error
        # else create the card and add it to the database
        if errors:
            return {
                "message": "Missing or sending incorrect data to create a card. Double check the JSON data that it has everything needed to create a card."
            }, 500
        else:
            card = create_card(form_data)
            db.session.add(card)
            db.session.commit()

        return {"message": "Card successfully created"}, 202


# Creates the routes for the classes
api.add_resource(CardData, "/cards/<int:card_id>")
api.add_resource(CardCreate, "/cards/create")
