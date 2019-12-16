from backend.models import Badge
from backend.general_utils import add_image


# Function to create a badge
def create_badge(form_data):
    file = form_data["image"]
    image = add_image(file, "badges")

    badge = Badge(name=form_data["name"],
                  description=form_data["description"],
                  image=image,
                  threshold=form_data["threshold"]
                  )

    return badge


# Function to edit a badge
def edit_badge(badge, form_data):
    badge.name = form_data["name"]
    badge.description = form_data["description"]
    badge.threshold = form_data["threshold"]
    badge.image = add_image(form_data["image"], "badges")

    return
