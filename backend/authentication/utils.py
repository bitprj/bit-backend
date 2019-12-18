from backend import guard
from backend.models import Admin, Student, Teacher


# Function to create an Admin
def create_admin(form_data):
    hashed_password = guard.hash_password(form_data["password"])

    admin = Admin(name=form_data["name"],
                  username=form_data["username"],
                  password=hashed_password,
                  roles="Admin",
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
                      image=form_data["image"]
                      )

    return student


# Function to create a Teacher
def create_teacher(form_data):
    hashed_password = guard.hash_password(form_data["password"])

    teacher = Teacher(name=form_data["name"],
                      username=form_data["username"],
                      password=hashed_password,
                      roles="Teacher",
                      location=form_data["location"],
                      image=form_data["image"]
                      )

    return teacher


# Function to choose which user to create, based on uer_type
def create_user(user_type, form_data):
    user = None

    if user_type == "Admin":
        user = create_admin(form_data)
    elif user_type == "Teacher":
        user = create_teacher(form_data)
    elif user_type == "Student":
        user = create_student(form_data)

    return user
