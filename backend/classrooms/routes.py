from backend import api, db, celery, app
from backend.activity_progresses.schemas import ActivityProgressSubmissionSerializer
from backend.authentication.decorators import roles_accepted
from backend.classrooms.decorators import classroom_exists, owns_classroom, valid_classroom_form
from backend.classrooms.schemas import ClassroomSerializer
from backend.classrooms.utils import create_classroom, edit_classroom, get_classroom_activities
from backend.models import Classroom
from backend.modules.utils import add_modules_to_students, get_modules
from backend.modules.decorators import valid_modules_list
from backend.teachers.utils import get_activities
from flask import Blueprint, request, session
from flask_restful import Resource

# Blueprint for classrooms
classrooms_bp = Blueprint("classrooms", __name__)


# Class for classroom CRUD routes
class ClassroomCRUD(Resource):
    method_decorators = [roles_accepted("Teacher", "Student"), classroom_exists]

    def get(self, classroom_id):
        classroom = Classroom.query.get(classroom_id)

        return ClassroomSerializer(classroom).data

    @celery.task(bind=True)
    def updateClassroom(self, classroom_id, form_data):
        with app.test_request_context():
            classroom = Classroom.query.get(classroom_id)
            edit_classroom(classroom, form_data)

            db.session.commit()

    # Function to edit a classroom
    @owns_classroom
    @valid_classroom_form
    def put(self, classroom_id):
        form_data = request.get_json()
        self.updateClassroom.delay(classroom_id, form_data)

        return {"message": "Classroom successfully updated"}, 200

    @celery.task(bind=True)
    def deleteClassroom(self, classroom_id):
        with app.test_request_context():
            classroom = Classroom.query.get(classroom_id)
            db.session.delete(classroom)
            db.session.commit()

    # Function to delete a classroom!!
    @owns_classroom
    def delete(self, classroom_id):
        self.deleteClassroom.delay(classroom_id)
        
        return {"message": "Classroom successfully deleted"}, 200


# This class is used to delete an classroom with a POST request
class ClassroomCreate(Resource):
    method_decorators = [roles_accepted("Teacher"), valid_classroom_form]

    # Function to create a classroom
    @celery.task(bind=True)
    def createClassroom(self, form_data, user_data):
        with app.test_request_context():
            classroom = create_classroom(form_data, user_data["teacher_id"])

            db.session.add(classroom)
            db.session.commit()

    def post(self):
        form_data = request.get_json()
        user_data = session["profile"]
        self.createClassroom.delay(form_data, user_data)

        return {"message": "Classroom successfully created"}, 202


# This class is used to update a classroom's modules
class ClassroomModules(Resource):
    method_decorators = [roles_accepted("Teacher"), owns_classroom, classroom_exists,
                         valid_modules_list]

    # Function to update a classroom's modules
    @celery.task(bind=True)
    def updateClassroomModules(self, data, classroom_id):
        with app.test_request_context():
            classroom = Classroom.query.get(classroom_id)
            modules = get_modules(data["module_ids"])
            add_modules_to_students(modules, classroom.students)
            classroom.modules = modules
            db.session.commit()


    def put(self, classroom_id):
        data = request.get_json()
        self.updateClassroomModules.delay(data, classroom_id)

        return {
                   "message": "Successfully updated classroom modules"
               }, 200


class ClassroomAssignments(Resource):
    method_decorators = [roles_accepted("Teacher"), owns_classroom, classroom_exists]

    # Function to display teacher data
    def get(self, classroom_id):
        classroom = Classroom.query.get(classroom_id)
        activity_set = get_classroom_activities(classroom)
        ungraded_assignments = get_activities(classroom.students, activity_set)

        if ungraded_assignments:
            return ActivityProgressSubmissionSerializer(ungraded_assignments, many=True).data

        return []


# Creates the routes for the classes
api.add_resource(ClassroomCRUD, "/classrooms/<int:classroom_id>")
api.add_resource(ClassroomCreate, "/classrooms")
api.add_resource(ClassroomModules, "/classrooms/<int:classroom_id>/modules")
api.add_resource(ClassroomAssignments, "/classrooms/<int:classroom_id>/activities")
