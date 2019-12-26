from flask import Blueprint
from flask_praetorian.decorators import roles_accepted
from flask_restful import Resource
from backend import api
from backend.general_utils import get_user_id_from_token
from backend.models import Student
from backend.students.schemas import student_schema

# Blueprint for students
students_bp = Blueprint("students", __name__)


# Class to display student data
class StudentInfo(Resource):
    method_decorators = [roles_accepted("Student")]

    # Function to display student data
    def get(self):
        current_user_id = get_user_id_from_token()
        student = Student.query.get(current_user_id)

        return student_schema.dump(student)


# Creates the routes for the classes
api.add_resource(StudentInfo, "/students/data")
