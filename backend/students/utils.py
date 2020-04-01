from backend.models import db, Activity, Checkpoint, UserActivity, UserCheckpoint
from datetime import datetime


# Function to create a student action based on the model type
def create_student_activity(model_obj, student, action):
    user_action = choose_action_type(model_obj, action)
    user_action.student_id = student.id
    db.session.add(user_action)
    db.session.commit()

    return user_action


# Function to choose an action type
def choose_action_type(model_obj, action):
    user_action = None

    if isinstance(model_obj, Activity):
        user_action = UserActivity(date_time=datetime.utcnow(),
                                   action=action)
        user_action.activity_id = model_obj.id
    elif isinstance(model_obj, Checkpoint):
        user_action = UserCheckpoint(date_time=datetime.utcnow(),
                                     action=action)
        user_action.checkpoint_id = model_obj.id

    return user_action


# Function to update a student's module progresses
def update_module_progresses(activity, student):
    topics = []
    completed_modules = set(student.completed_modules)
    inprogress_modules = set(student.inprogress_modules)
    incomplete_modules = set(student.incomplete_modules)

    for module in activity.modules:
        topics += module.topics

        if module in incomplete_modules:
            student.incomplete_modules.remove(module)

        if module not in completed_modules and module not in inprogress_modules:
            student.inprogress_modules.append(module)

    return topics


# Function to update a student's topic progresses
def update_topic_progresses(topics, student):
    completed_topics = set(student.completed_topics)
    inprogress_topics = set(student.inprogress_topics)

    for topic in topics:
        if topic not in completed_topics and topic not in inprogress_topics:
            student.inprogress_topics.append(topic)

    return
