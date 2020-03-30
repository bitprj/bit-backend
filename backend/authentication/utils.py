from backend import guard, mail, safe_url
from backend.models import Admin, Student, Teacher, User
from flask_mail import Message
from flask import url_for


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


# Function to get a list of users based on the username
def get_users(users):
    user_list = []

    for user in users:
        target_user = User.query.filter_by(username=user).first()
        user_list.append(target_user)

    return user_list


# Function to send an email verification email
def send_verification_email(email):
    token = safe_url.dumps(email, salt="email-confirm")
    msg = Message("Bit Project Email Confirmation", sender="info@bitproject.org", recipients=[email])
    link = url_for("userauthorize", token=token, _external=True)
    msg.body = "Click the following link to activate your account {}".format(link)
    mail.send(msg)

    return


# Function to send an email verification email
def send_graded_activity_email(email):
    msg = Message("Your Activity has been graded", sender="info@bitproject.org",
                  recipients=[email])
    # CHANGE THIS TO POINT TO THE STUDENT PORTAL IN THE FRONTEND
    link = url_for("studentinfo", _external=True)
    msg.body = "Please go visit your student portal to see your grade {}".format(link)
    mail.send(msg)

    return
