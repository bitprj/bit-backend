from backend.models import Module, Student, Topic
from backend.prereqs.fetch import get_activities, get_modules
from backend.prereqs.utils import assign_badge_prereqs, delete_badge_prereqs


# Function to create a topic
def create_topic(form_data):
    topic = Topic(name=form_data["name"],
                  description=form_data["description"]
                  )

    topic.activity_prereqs = get_activities(form_data["activity_prereqs"])
    topic.modules = get_modules(form_data["modules"])
    topic.module_prereqs = get_modules(form_data["module_prereqs"])

    return topic


# Function to edit a topic
def edit_topic(topic, form_data):
    topic.name = form_data["name"]
    topic.description = form_data["description"]
    topic.activity_prereqs = get_activities(form_data["activity_prereqs"])
    topic.modules = get_modules(form_data["modules"])
    topic.module_prereqs = get_modules(form_data["module_prereqs"])
    delete_badge_prereqs(topic)
    assign_badge_prereqs(form_data["badge_prereqs"], topic, "Topic")

    return


# Function to get the student's topic progress based on topic id
def get_topic_progress(student_id, topic_id):
    student = Student.query.get(student_id)
    modules = set(Module.query.filter(Module.topics.any(id=topic_id)).all())
    completed_modules = set(student.completed_modules).intersection(modules)
    incomplete_modules = set(student.incomplete_modules).intersection(modules)

    module_progress = {"completed_modules": completed_modules,
                       "incomplete_modules": incomplete_modules}

    return module_progress


# Function to check if a topic exists in the database
def validate_topic(track_id):
    topic = Topic.query.get(track_id)

    if not topic:
        return True

    return False
