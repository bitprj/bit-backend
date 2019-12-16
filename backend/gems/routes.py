from flask import (Blueprint, jsonify, request)
from flask_restful import Resource
from backend import api, db
from backend.gems.schemas import gem_schema
from backend.gems.utils import create_gem, edit_gem
from backend.models import Gem


# Blueprint for gems
gems_bp = Blueprint("gems", __name__)


# Class to Read, Update, and Destroy routes
class GemData(Resource):
    # Function to return data on a single gem
    def get(self, gem_id):
        gem = Gem.query.get(gem_id)

        # If gem does not exists, then return a 404 error
        # else return the gem back to the user
        if not gem:
            return {"message": "Gem does not exist"}, 404
        else:
            return gem_schema.dump(gem)

    # Function to edit a gem
    def put(self, gem_id):
        gem = Gem.query.get(gem_id)

        # If gem does not exist, then return a 404 error
        # else edit a gem and edit it in the database
        if not gem:
            return {"message": "Gem does not exist"}, 404
        else:
            form_data = request.get_json()
            errors = gem_schema.validate(form_data)

            # If form data is not validated by the gem_schema, then return a 500 error
            # else edit the gem and save it to the database
            if errors:
                return {
                            "message": "Missing or sending incorrect data to edit a gem. Double check the JSON data that it has everything needed to edit a gem."
                       }, 500
            else:
                edit_gem(gem, form_data)
                db.session.commit()

                return {"message": "Gem successfully updated"}, 202

    # Function to delete a gem
    def delete(self, gem_id):
        gem = Gem.query.get(gem_id)

        # If gem does not exists, return a 404 error
        # else delete the gem and save to database
        if not gem:
            return {"message": "Gem does not exist"}, 404
        else:
            db.session.delete(gem)
            db.session.commit()

        return {"message": "Gem successfully deleted"}, 200


# Class to define gem creation
class GemCreate(Resource):
    # Function to create a gem
    def post(self):
        gem = create_gem()
        db.session.add(gem)
        db.session.commit()

        return {"message": "Gem successfully created"}, 202


# Creates the routes for the classes
api.add_resource(GemData, "/gems/<int:gem_id>")
api.add_resource(GemCreate, "/gems/create")
