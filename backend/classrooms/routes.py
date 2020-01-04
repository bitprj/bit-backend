from flask import (Blueprint, request)
from flask_restful import Resource
from backend import api, db
from backend.classrooms.schemas import classroom_form_schema
from backend.classrooms.utils import create_classroom, edit_classroom
from backend.models import Classroom


# Blueprint for classrooms
classrooms_bp = Blueprint("classrooms", __name__)


# Class for classroom CRUD routes
class ClassroomCRUD(Resource):
    def get(self, classroom_id):
        classroom = Classroom.query.get(classroom_id)

        if not classroom:
            return {"message": "Classroom does not exist"}, 404

        return classroom_schema.dump(classroom)
    
    # Function to edit an classroom
    def put(self, classroom_id):
        form_data = request.get_json()
        classroom = Classroom.query.get(classroom_id)
        error
        edit_classroom(classroom, form_data)

        db.session.commit()

        return {"message": "Classroom successfully updated"}, 200

    # Function to delete a classroom!!
    def delete(self, classroom_id):
        form_data = request.get_json()
        classroom = Classroom.query.get(classroom_id)

        if not classroom:
            return {"message": "Classroom does not exist"}, 404

        db.session.delete(classroom)
        db.session.commit()

        return {"message": "Classroom successfully deleted"}, 200


# This class is used to delete an classroom with a POST request
class ClassroomCreate(Resource):
    # Function to create a classroom
    def post(self):
        form_data = request.get_json()
        classroom = create_classroom(form_data)

        db.session.add(classroom)
        db.session.commit()

        return {"message": "Classroom successfully created"}, 201


# Creates the routes for the classes
api.add_resource(ClassroomCRUD, "/classrooms/<int:classroom_id>")
api.add_resource(ClassroomCreate, "/classrooms/delete")
