from flask import (Blueprint, request)
from flask_restful import Resource
from backend import api, db
from backend.models import Badge, badge_schema
from backend.general_utils import add_image

# Blueprint for badges
badges_bp = Blueprint("badges", __name__)


# Class to define all of the Badge CRUD routes
class BadgeData(Resource):
    # Function to return data on a single badge
    def get(self, badge_id):
        badge = Badge.query.get(badge_id)

        return badge_schema.jsonify(badge)

    # Function to edit a badge
    def put(self, badge_id):
        form_data = request.get_json()
        badge = Badge.query.get(badge_id)
        levels = {"2": form_data["level_two"], "3": form_data["level_three"], "4": form_data["level_four"],
                  "5": form_data["level_five"]}
        badge.name = form_data["name"]
        badge.description = form_data["description"]
        badge.threshold = levels
        badge.image = add_image(form_data["file"], "badges")
        db.session.commit()

        return {"message": "Badge successfully updated"}, 202

    # Function to delete a badge
    def delete(self, badge_id):
        badge = Badge.query.get(badge_id)
        db.session.delete(badge)
        db.session.commit()

        return {"message": "Badge successfully deleted"}, 200


class BadgeCreate(Resource):
    # Function to create a badge
    def post(self):
        form_data = request.get_json()
        levels = {}
        file = form_data["file"]
        image = add_image(file, "badges")
        levels["2"] = form_data["level_two"]
        levels["3"] = form_data["level_three"]
        levels["4"] = form_data["level_four"]
        levels["5"] = form_data["level_five"]

        badge = Badge(name=form_data["name"],
                      description=form_data["description"],
                      image=image,
                      threshold=levels
                      )
        db.session.add(badge)
        db.session.commit()

        return {"message": "Badge successfully created"}, 202


api.add_resource(BadgeData, "/badges/<int:badge_id>")
api.add_resource(BadgeCreate, "/badges/create")

