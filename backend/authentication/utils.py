from backend import guard
from backend.models import Admin, Classroom, Student, Teacher, Track
from backend.prereqs.utils import assign_incomcomplete_activities, assign_incomplete_modules


# Function to create an Admin
def create_admin(form_data):
    hashed_password = guard.hash_password(form_data["password"])

    admin = Admin(name=form_data["name"],
                  username=form_data["username"],
                  password=hashed_password,
                  roles="Admin",
                  is_active=False,
                  location=form_data["location"],
                  image=form_data["image"]
                  )

    return admin


# Function to create a Student
def create_student(form_data):
    hashed_password = guard.hash_password(form_data["password"])

    student = Student(name=form_data["name"],
                      username=form_data["username"],
                      password=hashed_password,
                      roles="Student",
                      location=form_data["location"],
                      is_active=False,
                      image=form_data["image"],
                      current_track_id=form_data["track_id"]
                      )

    classroom = Classroom.query.filter_by(class_code=form_data["class_code"]).first()
    student.classes.append(classroom)
    track = Track.query.get(form_data["track_id"])
    student.incomplete_topics = track.topics
    student.incomplete_modules = assign_incomplete_modules(track.topics)
    student.incomplete_activities = assign_incomcomplete_activities(track.topics)

    return student


# Function to create a Teacher
def create_teacher(form_data):
    hashed_password = guard.hash_password(form_data["password"])

    teacher = Teacher(name=form_data["name"],
                      username=form_data["username"],
                      password=hashed_password,
                      roles="Teacher",
                      is_active=False,
                      location=form_data["location"],
                      image=form_data["image"]
                      )

    return teacher


# Function to choose which user to create, based on user_type
def create_user(user_type, form_data):
    user = None

    if user_type == "Admin":
        user = create_admin(form_data)
    elif user_type == "Teacher":
        user = create_teacher(form_data)
    elif user_type == "Student":
        user = create_student(form_data)

    return user
