from backend.models import Classroom
import random
import string


# Function to create a classroom
def create_classroom(form_data):
    classroom = Classroom(name=form_data["name"],
                          date_start=form_data["date_start"],
                          date_end=form_data["data_end"]
                          )

    code = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(5)])
    classroom.code = code

    return classroom


# Function to edit a classroom
def edit_classroom(classroom, form_data):
    classroom.name = form_data["parameters"]["name"]["en-US"]

    return
