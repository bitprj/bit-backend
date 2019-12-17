from backend.models import User


# Function to validate whether or not a user already exist in the database
def check_user_existence(username):
    user = User.query.filter_by(username=username).first()

    if user:
        return True
    else:
        return False
