from flask import (Blueprint, request)
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from backend import api, db
from backend.authentication.decorators import roles_accepted
from backend.classrooms.decorators import classroom_exists, owns_classroom, valid_classroom_form
from backend.classrooms.schemas import classroom_schema
from backend.classrooms.utils import create_classroom, edit_classroom
from backend.models import Classroom, Teacher
from backend.modules.utils import get_modules
from backend.modules.decorators import valid_modules_list

# Blueprint for classrooms
classrooms_bp = Blueprint("classrooms", __name__)


# Class for classroom CRUD routes
class ClassroomCRUD(Resource):
    method_decorators = [roles_accepted("Teacher"), jwt_required, classroom_exists]

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
        username = get_jwt_identity()
        teacher = Teacher.query.filter_by(username=username).first()
        classroom = create_classroom(form_data, teacher.id)

        db.session.add(classroom)
        db.session.commit()

        return {"message": "Classroom successfully created"}, 202


# This class is used to update a classroom's modules
class ClassroomModules(Resource):
    method_decorators = [roles_accepted("Teacher"), classroom_exists, valid_modules_list]

    # Function to update a classroom's modules
    @owns_classroom
    def put(self, classroom_id):
        data = request.get_json()
        classroom = Classroom.query.get(classroom_id)
        modules = get_modules(data["module_ids"])
        classroom.modules = modules

        return {
                   "message": "Successfully updated classroom modules"
               }, 200


# Creates the routes for the classes
api.add_resource(ClassroomCRUD, "/classrooms/<int:classroom_id>")
api.add_resource(ClassroomCreate, "/classrooms/create")
api.add_resource(ClassroomModules, "/classrooms/<int:classroom_id>/modules")
