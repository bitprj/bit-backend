from flask import (Blueprint, session)
from flask_restful import Resource
from backend import api, db
from backend.authentication.decorators import roles_accepted
from backend.models import Module, Student
from backend.modules.decorators import module_exists, module_is_incomplete, module_is_complete, module_in_inprogress
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
        username = session["username"]
        student = Student.query.filter_by(username=username).first()
        topic_progress = get_topic_progress(student.id, topic_id)

        return topic_progress_schema.dump(topic_progress)


# Class to add a module to a student's inprogress_module
class TopicProgressAdd(Resource):
    method_decorators = [roles_accepted("Student"), module_exists]

    # Function to add a module to a student's inprogress_modules
    @module_is_incomplete
    def put(self, topic_id, module_id):
        username = session["username"]
        student = Student.query.filter_by(username=username).first()
        module = Module.query.get(module_id)
        student.inprogress_modules.append(module)
        student.incomplete_modules.remove(module)

        db.session.commit()

        return {
                   "message": "Module added!"
               }, 201


# Class to update the student's TopicProgress
class TopicProgressUpdate(Resource):
    method_decorators = [roles_accepted("Student"), topic_exists, module_exists]

    # Function to update the student's completed module
    @module_is_complete
    @module_in_inprogress
    def put(self, topic_id, module_id):
        username = session["username"]
        student = Student.query.filter_by(username=username).first()
        module = Module.query.get(module_id)
        student.completed_modules.append(module)
        student.inprogress_modules.remove(module)

        db.session.commit()

        return {
                   "message": "Successfully updated student completed modules"
               }, 202


api.add_resource(TopicProgress, "/topics/<int:topic_id>/progress")
api.add_resource(TopicProgressAdd, "/topics/<int:topic_id>/progress/<int:module_id>/add")
api.add_resource(TopicProgressUpdate, "/topics/<int:topic_id>/progress/<int:module_id>")
