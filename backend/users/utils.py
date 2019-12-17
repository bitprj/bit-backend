from backend import bcrypt, guard
from backend.models import Admin


# Function to create an admin
def create_admin(form_data):
    hashed_password = guard.hash_password(form_data["password"])

    admin = Admin(name=form_data["name"],
                  email=form_data["email"],
                  password=hashed_password,
                  roles="Admin",
                  location=form_data["location"],
                  image=form_data["image"]
                  )

    return admin
