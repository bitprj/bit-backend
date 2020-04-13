from backend import api, db
from backend.authentication.decorators import roles_required, user_session_exists
from backend.classrooms.decorators import valid_classroom_code, valid_classroom_code_form
from backend.models import Classroom, Student
from backend.module_progresses.utils import can_create_module_progress
from backend.students.decorators import student_exists, valid_update_data
from backend.students.schemas import StudentSerializer, StudentClassroomSerializer
from backend.students.utils import update_student_suggested_activity
from datetime import datetime
from flask import Blueprint, request, session
from flask_restful import Resource


# Blueprint for students
students_bp = Blueprint("students", __name__)


# This class is used to let a student join a classroom
class StudentClassroom(Resource):
    method_decorators = [roles_required("Student"), valid_classroom_code, valid_classroom_code_form]

    def put(self):
        data = request.get_json()
        user_data = session["profile"]
        student = Student.query.get(user_data["student_id"])
        classroom = Classroom.query.filter_by(class_code=data["class_code"]).first()
        student.classes.append(classroom)
        student.incomplete_modules += classroom.modules

        for module in classroom.modules:
            module_prog = can_create_module_progress(student, module)
            db.session.add(module_prog)
        db.session.commit()

        return {
            "messaged": "Classroom joined"
        }, 200


# Class to display student data
class StudentData(Resource):
    method_decorators = [user_session_exists]

    # Function to display student data
    @student_exists
    def get(self, student_id):
        student = Student.query.get(student_id)
        classroom_id = request.args.get("classroom_id")

        if classroom_id:
            student_data = StudentClassroomSerializer(student).data
        elif student_id == session["profile"]["student_id"]:
            student_data = StudentSerializer(student).data
            student_data["suggested_activity"] = update_student_suggested_activity(student)
            student.meta.user.last_seen = datetime.utcnow()
            db.session.commit()
        else:
            student_data = StudentSerializer(student).data
            student_data["suggested_activity"] = update_student_suggested_activity(student)

        return student_data

    # Function to edit student_data
    @valid_update_data
    def put(self):
        data = request.get_json()
        user_data = session["profile"]
        student = Student.query.get(user_data["id"])
        student.suggested_activity_id = data["suggested_activity"]["id"]
        student.suggested_module_id = data["suggested_activity"]["module_id"]
        student_data = StudentSerializer(student).data
        student_data["suggested_activity"] = data["suggested_activity"]
        db.session.commit()

        return student_data


# Creates the routes for the classes
api.add_resource(StudentData, "/students/<int:student_id>")
api.add_resource(StudentClassroom, "/students/classrooms")
