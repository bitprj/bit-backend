from backend import mail
from backend.models import User
from flask_mail import Message
from flask import url_for


# Function to choose which user to create, based on user_type
def create_user(oauth_user_data, oauth_emails, access_token, meta_id):
    user = User(name=oauth_user_data["name"],
                email=oauth_emails[0]["email"],
                image=oauth_user_data["avatar_url"],
                github_id=oauth_user_data["id"],
                github_username=oauth_user_data["login"],
                github_access_token=access_token,
                meta_id=meta_id
                )

    return user


# Function to get a list of users based on the username
def get_users(users):
    user_list = []

    for user in users:
        target_user = User.query.filter_by(username=user).first()
        user_list.append(target_user)

    return user_list


# Function to send an email verification email
def send_graded_activity_email(email):
    msg = Message("Your Activity has been graded", sender="info@bitproject.org",
                  recipients=[email])
    # CHANGE THIS TO POINT TO THE STUDENT PORTAL IN THE FRONTEND
    link = url_for("studentinfo", _external=True)
    msg.body = "Please go visit your student portal to see your grade {}".format(link)
    mail.send(msg)

    return
