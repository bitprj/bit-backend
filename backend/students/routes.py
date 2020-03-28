from flask import (Blueprint, request, session)
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity
from flask_restful import Resource
from backend import api, db
from backend.authentication.decorators import roles_accepted
from backend.classrooms.decorators import valid_classroom_code, valid_classroom_code_form
from backend.models import Classroom, Student
from backend.students.schemas import student_schema

# Blueprint for students
students_bp = Blueprint("students", __name__)


# This class is used to update the student's classrooms
class StudentClassroom(Resource):
    method_decorators = [roles_accepted("Student"), valid_classroom_code, valid_classroom_code_form]

    def put(self):
        data = request.get_json()
        username = get_jwt_identity()
        student = Student.query.filter_by(username=username).first()
        classroom = Classroom.query.filter_by(class_code=data["class_code"]).first()
        student.classrooms.append(classroom)
        student.incomplete_modules += classroom.modules
        db.session.commit()

        return


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
api.add_resource(StudentClassroom, "/students/classrooms")
