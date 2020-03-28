<<<<<<< HEAD
from flask import (Blueprint, request, session)
=======
from flask import Blueprint
>>>>>>> parent of cf3cf07... Bryan w (#56)
from flask_jwt_extended import get_jwt_identity
from flask_restful import Resource
from backend import api
from backend.authentication.decorators import roles_accepted
from backend.models import Student
from backend.students.schemas import student_schema

# Blueprint for students
students_bp = Blueprint("students", __name__)


# Class to display student data
class StudentInfo(Resource):
    method_decorators = [roles_accepted("Student")]

    # Function to display student data
    def get(self):
        username = session["profile"]["username"]
        student = Student.query.filter_by(username=username).first()

        return student_schema.dump(student)


# Creates the routes for the classes
api.add_resource(StudentInfo, "/students/data")
