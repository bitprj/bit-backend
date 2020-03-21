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
    class_code = fields.Str(required=False)

    class Meta:
        # Fields to show when sending data
        fields = ("name", "username", "password", "roles", "location", "image", "track_id", "class_code")
        ordered = True


# This schema is used to display user data,
class UserSchema(ma.Schema):
    id = fields.Str(required=True)
    name = fields.Str(required=True)
    username = fields.Email(required=True)
    location = fields.Str(required=True)
    roles = fields.Str(required=False)
    image = fields.Str(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "name", "username", "roles", "location", "image")
        ordered = True


# This schema is used to validate user login information
class UserLoginSchema(ma.Schema):
    username = fields.Email(required=True)
    password = fields.Str(required=True)


user_form_schema = UserFormSchema()
user_schema = UserSchema()
user_login_schema = UserLoginSchema()
