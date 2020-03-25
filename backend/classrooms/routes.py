from flask import (Blueprint, request, session)
from flask_restful import Resource
from backend import api, db
from backend.authentication.decorators import auth0_auth, roles_accepted
from backend.classrooms.decorators import classroom_exists, owns_classroom, valid_classroom_form
from backend.classrooms.schemas import classroom_schema
from backend.classrooms.utils import create_classroom, edit_classroom
from backend.models import Classroom, Teacher

# Blueprint for classrooms
classrooms_bp = Blueprint("classrooms", __name__)


# Class for classroom CRUD routes
class ClassroomCRUD(Resource):
    method_decorators = [roles_accepted("Teacher"), auth0_auth, classroom_exists]

    @owns_classroom
    def get(self, classroom_id):
        classroom = Classroom.query.get(classroom_id)

        return classroom_schema.dump(classroom)

    # Function to edit a classroom
    @owns_classroom
    @valid_classroom_form
    def put(self, classroom_id):
        classroom = Classroom.query.get(classroom_id)
        form_data = request.get_json()
        edit_classroom(classroom, form_data)

        db.session.commit()

        return {"message": "Classroom successfully updated"}, 202

    # Function to delete a classroom!!
    @owns_classroom
    def delete(self, classroom_id):
        classroom = Classroom.query.get(classroom_id)

        db.session.delete(classroom)
        db.session.commit()

        return {"message": "Classroom successfully deleted"}, 200


# This class is used to delete an classroom with a POST request
class ClassroomCreate(Resource):
    method_decorators = [roles_accepted("Teacher"), valid_classroom_form]

    # Function to create a classroom
    def post(self):
        form_data = request.get_json()
        username = session["username"]
        teacher = Teacher.query.filter_by(username=username).first()
        classroom = create_classroom(form_data, teacher.id)

        db.session.add(classroom)
        db.session.commit()

        return {"message": "Classroom successfully created"}, 202


# Creates the routes for the classes
api.add_resource(ClassroomCRUD, "/classrooms/<int:classroom_id>")
api.add_resource(ClassroomCreate, "/classrooms/create")
