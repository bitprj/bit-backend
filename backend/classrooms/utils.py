from backend.models import Classroom
import random
import string


# Function to create a classroom
def create_classroom(form_data, teacher_id):
    classroom = Classroom(name=form_data["name"],
                          teacher_id=teacher_id,
                          date_start=form_data["date_start"],
                          date_end=form_data["date_end"]
                          )

    code = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(5)])
    classroom.class_code = code

    return classroom


# Function to edit a classroom
def edit_classroom(classroom, form_data):
    classroom.name = form_data["name"]
    classroom.date_start = form_data["date_start"]
    classroom.date_end = form_data["date_end"]

    return
