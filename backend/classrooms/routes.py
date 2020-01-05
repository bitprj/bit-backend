from flask import (Blueprint, request)
from flask_praetorian.decorators import roles_accepted
from flask_restful import Resource
from backend import api, db
from backend.classrooms.schemas import classroom_form_schema, classroom_schema
from backend.classrooms.utils import create_classroom, edit_classroom, owns_classroom
from backend.general_utils import get_user_id_from_token
from backend.models import Classroom

# Blueprint for classrooms
classrooms_bp = Blueprint("classrooms", __name__)


# Class for classroom CRUD routes
class ClassroomCRUD(Resource):
    method_decorators = [roles_accepted("Teacher")]

    def get(self, classroom_id):
        classroom = Classroom.query.get(classroom_id)

        if not classroom:
            return {"message": "Classroom does not exist"}, 404

        return classroom_schema.dump(classroom)

    # Function to edit a classroom
    def put(self, classroom_id):
        classroom = Classroom.query.get(classroom_id)

        # If classroom does not exist, then return a 404 error
        # else edit a classroom and edit it in the database
        if not classroom:
            return {"message": "Classroom does not exist"}, 404
        else:
            current_user_id = get_user_id_from_token()
            teacher_owns_classroom = owns_classroom(classroom, current_user_id)

            if teacher_owns_classroom:
                form_data = request.get_json()
                errors = classroom_form_schema.validate(form_data)

                # If form data is not validated by the classroom_schema, then return a 500 error
                # else edit the classroom and save it to the database
                if errors:
                    return {
                               "message": "Missing or sending incorrect data to edit a classroom. Double check the JSON data that it has everything needed to edit a classroom."
                           }, 500
                else:
                    edit_classroom(classroom, form_data)
                    db.session.commit()
            else:
                return {
                           "message": "You do not own this classroom"
                       }, 500

            return {"message": "Classroom successfully updated"}, 202

    # Function to delete a classroom!!
    def delete(self, classroom_id):
        classroom = Classroom.query.get(classroom_id)
        current_user_id = get_user_id_from_token()

        if not classroom:
            return {"message": "Classroom does not exist"}, 404

        teacher_owns_classroom = owns_classroom(classroom, current_user_id)

        if teacher_owns_classroom:
            db.session.delete(classroom)
            db.session.commit()
        else:
            return {
                       "message": "You do not own this classroom"
                   }, 500

        return {"message": "Classroom successfully deleted"}, 200


# This class is used to delete an classroom with a POST request
class ClassroomCreate(Resource):
    method_decorators = [roles_accepted("Teacher")]

    # Function to create a classroom
    def post(self):
        form_data = request.get_json()
        current_user_id = get_user_id_from_token()
        errors = classroom_form_schema.validate(form_data)

        # If form data is not validated by the classroom_schema, then return a 500 error
        # else create the classroom and add it to the database
        if errors:
            return {
                       "message": "Missing or sending incorrect data to create a classroom. Double check the JSON data that it has everything needed to create a classroom."
                   }, 500
        else:
            classroom = create_classroom(form_data, current_user_id)
            db.session.add(classroom)
            db.session.commit()

        return {"message": "Classroom successfully created"}, 202


# Creates the routes for the classes
api.add_resource(ClassroomCRUD, "/classrooms/<int:classroom_id>")
api.add_resource(ClassroomCreate, "/classrooms/create")
