from flask import (Blueprint, request, session)
from flask_restful import Resource
from backend import api, db
from backend.authentication.decorators import auth0_auth, roles_accepted
from backend.activity_progresses.schemas import activity_progress_submission_schema
from backend.classrooms.decorators import classroom_exists, owns_classroom, valid_classroom_form
from backend.classrooms.schemas import classroom_schema
from backend.classrooms.utils import create_classroom, edit_classroom, get_classroom_activities
from backend.models import Classroom, Teacher
from backend.modules.utils import get_modules
from backend.modules.decorators import valid_modules_list
from backend.teachers.utils import get_activities

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
        username = session["profile"]["username"]
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
        db.session.commit()

        return {
                   "message": "Successfully updated classroom modules"
               }, 200


class ClassroomAssignments(Resource):
    method_decorators = [roles_accepted("Teacher"), classroom_exists]

    # Function to display teacher data
    @owns_classroom
    def get(self, classroom_id):
        classroom = Classroom.query.get(classroom_id)
        activity_set = get_classroom_activities(classroom)
        ungraded_assignments = get_activities(classroom.students, activity_set)

        if ungraded_assignments:
            return activity_progress_submission_schema.dump(ungraded_assignments)

        return []


# Creates the routes for the classes
api.add_resource(ClassroomCRUD, "/classrooms/<int:classroom_id>")
api.add_resource(ClassroomCreate, "/classrooms")
api.add_resource(ClassroomModules, "/classrooms/<int:classroom_id>/modules")
api.add_resource(ClassroomAssignments, "/classrooms/<int:classroom_id>/activities")
