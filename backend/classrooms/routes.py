from flask import (Blueprint, request)
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from backend import api, db
from backend.authentication.decorators import roles_accepted
from backend.classrooms.decorators import classroom_exists, valid_classroom_form
from backend.classrooms.schemas import classroom_schema
from backend.classrooms.utils import create_classroom, edit_classroom, owns_classroom
from backend.models import Classroom, Teacher

# Blueprint for classrooms
classrooms_bp = Blueprint("classrooms", __name__)


# Class for classroom CRUD routes
class ClassroomCRUD(Resource):
    method_decorators = [roles_accepted("Teacher"), jwt_required, classroom_exists]

    def get(self, classroom_id):
        owns_class = owns_classroom(classroom_id)

        if owns_class:
            classroom = Classroom.query.get(classroom_id)
        else:
            return {
                       "message": "You do not own this classroom"
                   }, 500

        return classroom_schema.dump(classroom)

    # Function to edit a classroom
    @valid_classroom_form
    def put(self, classroom_id):
        owns_class = owns_classroom(classroom_id)

        if owns_class:
            classroom = Classroom.query.get(classroom_id)
            form_data = request.get_json()
            edit_classroom(classroom, form_data)

            db.session.commit()
        else:
            return {
                       "message": "You do not own this classroom"
                   }, 500

        return {"message": "Classroom successfully updated"}, 202

    # Function to delete a classroom!!
    def delete(self, classroom_id):
        owns_class = owns_classroom(classroom_id)

        if owns_class:
            classroom = Classroom.query.get(classroom_id)

            db.session.delete(classroom)
            db.session.commit()
        else:
            return {
                       "message": "You do not own this classroom"
                   }, 500

        return {"message": "Classroom successfully deleted"}, 200


# This class is used to delete an classroom with a POST request
class ClassroomCreate(Resource):
    method_decorators = [roles_accepted("Teacher"), valid_classroom_form]

    # Function to create a classroom
    def post(self):
        form_data = request.get_json()
        username = get_jwt_identity()
        teacher = Teacher.query.filter_by(username=username).first()
        classroom = create_classroom(form_data, teacher.id)

        db.session.add(classroom)
        db.session.commit()

        return {"message": "Classroom successfully created"}, 202


# Creates the routes for the classes
api.add_resource(ClassroomCRUD, "/classrooms/<int:classroom_id>")
api.add_resource(ClassroomCreate, "/classrooms/create")
