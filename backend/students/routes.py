from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from backend import api, db
from backend.authentication.decorators import roles_required
from backend.classrooms.decorators import valid_classroom_code, valid_classroom_code_form
from backend.models import Classroom, Student
from backend.students.decorators import student_exists
from backend.students.schemas import student_classroom_schema, student_schema
from datetime import datetime

# Blueprint for students
students_bp = Blueprint("students", __name__)


# This class is used to update the student's classrooms
class StudentClassroom(Resource):
    method_decorators = [roles_required("Student"), valid_classroom_code, valid_classroom_code_form]

    def put(self):
        data = request.get_json()
        username = get_jwt_identity()
        student = Student.query.filter_by(username=username).first()
        classroom = Classroom.query.filter_by(class_code=data["class_code"]).first()
        student.classes.append(classroom)
        student.incomplete_modules += classroom.modules
        db.session.commit()

        return {
            "messaged": "Classroom joined"
        }, 200


# Class to display student data
class StudentInfo(Resource):
    method_decorators = [jwt_required]

    # Function to display student data
    @student_exists
    def get(self):
        student_id = request.args.get("student_id")
        classroom_id = request.args.get("classroom_id")
        student_data = None

        if student_id and classroom_id:
            student = Student.query.get(student_id)
            student_data = student_classroom_schema.dump(student)
        elif student_id and not classroom_id:
            student = Student.query.get(student_id)
            student_data = student_schema.dump(student)
        elif not student_id and not classroom_id:
            username = get_jwt_identity()
            student = Student.query.filter_by(username=username).first()
            student_data = student_schema.dump(student)
            student.last_seen = datetime.utcnow()
            db.session.commit()

        return student_data


# Creates the routes for the classes
api.add_resource(StudentInfo, "/students/data")
api.add_resource(StudentClassroom, "/students/classrooms")
