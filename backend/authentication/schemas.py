from backend import ma
from marshmallow import fields


# This schema is used to validate data to create a user
class UserFormSchema(ma.Schema):
    name = fields.Str(required=True)
    username = fields.Email(required=True)
    password = fields.Str(required=True)
    roles = fields.Str(required=False)
    location = fields.Str(required=True)
    image = fields.Str(required=True)
    track_id = fields.Int(required=False)

    class Meta:
        # Fields to show when sending data
        fields = ("name", "username", "password", "roles", "location", "image", "track_id")
        ordered = True


# This schema is used to display user data,
# Don't want to expose private data like its id, or password
class UserSchema(ma.Schema):
    name = fields.Str(required=True)
    username = fields.Email(required=True)
    location = fields.Str(required=True)
    roles = fields.Str(required=False)
    image = fields.Str(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("name", "username", "roles", "location", "image")
        ordered = True


# This schema is used to validate user login information
class UserLoginSchema(ma.Schema):
    username = fields.Email(required=True)
    password = fields.Str(required=True)


user_form_schema = UserFormSchema()
user_schema = UserSchema()
user_login_schema = UserLoginSchema()
