from flask import Blueprint
from flask_jwt_extended import get_jwt_identity
from flask_restful import Resource
from backend import api, db
from backend.authentication.decorators import roles_accepted
from backend.models import Module, Student
from backend.modules.decorators import module_exists
from backend.topics.decorators import topic_exists
from backend.topics.utils import get_topic_progress
from backend.topic_progresses.schemas import topic_progress_schema

# Blueprint for topics
topic_progresses_bp = Blueprint("topic_progresses", __name__)


# Class for topic progress
class TopicProgress(Resource):
    method_decorators = [roles_accepted("Student"), topic_exists]

    # Function to retrieve the module progress for a student given an id
    def get(self, topic_id):
        username = get_jwt_identity()
        student = Student.query.filter_by(username=username).first()

        topic_progress = get_topic_progress(student.id, topic_id)
        return topic_progress_schema.dump(topic_progress)


# Class to add a module to a student's inprogress_module
class TopicProgressAdd(Resource):
    method_decorators = [roles_accepted("Student"), module_exists]

    # Function to add a module to a student's inprogress_modules
    def put(self, topic_id, module_id):
        username = get_jwt_identity()
        student = Student.query.filter_by(username=username).first()
        module = Module.query.get(module_id)
        student.inprogress_modules.append(module)

        if module in student.incomplete_modules:
            student.inprogress_modules.remove(module)

        db.session.commit()

        return {
                   "message": "Module added!"
               }, 201


# Class to update the student's TopicProgress
class TopicProgressUpdate(Resource):
    method_decorators = [roles_accepted("Student"), topic_exists, module_exists]

    # Function to update the student's completed module
    def put(self, topic_id, module_id):
        username = get_jwt_identity()
        student = Student.query.filter_by(username=username).first()
        module = Module.query.get(module_id)

        if module not in student.incomplete_modules:
            return {
                       "message": "Module does not exist in the student's incomplete modules."
                   }, 500
        else:
            student.completed_modules.append(module)
            student.incomplete_modules.remove(module)
            db.session.commit()

        return {
                   "message": "Successfully updated student completed modules"
               }, 202


api.add_resource(TopicProgress, "/topics/<int:topic_id>/progress")
api.add_resource(TopicProgressAdd, "/topics/<int:topic_id>/progress/<int:module_id>/add")
api.add_resource(TopicProgressUpdate, "/topics/<int:topic_id>/progress/<int:module_id>")
