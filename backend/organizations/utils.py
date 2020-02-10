from backend.general_utils import add_file
from backend.models import Organization


# Function to create a organization
def create_organization(form_data, images, user):
    image = add_file(images["image"], "organizations")
    background_image = add_file(images["background_image"], "organizations")
    organization = Organization(name=form_data["name"],
                                image=image,
                                background_image=background_image,
                                is_active=True
                                )
    organization.owners.append(user)

    return organization


# Function to edit a organization
def edit_organization(organization, form_data, images):
    image = add_file(images["image"], "organizations")
    background_image = add_file(images["background_image"], "organizations")
    organization.name = form_data["name"]
    organization.image = image
    organization.background_image = background_image

    return
