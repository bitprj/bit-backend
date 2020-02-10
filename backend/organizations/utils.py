from flask import url_for
from flask_mail import Message
from backend import mail, safe_url
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
    organization.active_users.append(user)

    return organization


# Function to edit a organization
def edit_organization(organization, form_data, images):
    image = add_file(images["image"], "organizations")
    background_image = add_file(images["background_image"], "organizations")
    organization.name = form_data["name"]
    organization.image = image
    organization.background_image = background_image

    return


# Function to remove a user from an organization
def remove_user(organization, user):
    if user in organization.active_users:
        organization.active_users.remove(user)

    if user in organization.inactive_users:
        organization.inactive_users.remove(user)

    if user in organization.owners:
        organization.owners.remove(user)

    return


# Function to send
def send_invites(users, organization):
    with mail.connect() as conn:
        for user in users:
            msg = send_owner_invitation(user, organization)
            conn.send(msg)
    return


# Function to send an email verification email
def send_owner_invitation(email, organization):
    info = {"email": email, "organization_id": organization.id}
    token = safe_url.dumps(info, salt="owner_invite")
    msg = Message("Organization Invite", sender="info@bitproject.org", recipients=[email])
    link = url_for("organizationinviteconfirm", token=token, _external=True)
    msg.body = "You have been invited to join " + organization.name + " as an owner " + "{}".format(link)

    return msg
