from backend import ma
from marshmallow import fields


class UserFormSchema(ma.Schema):
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("name", "email", "password")
        ordered = True


class UserSchema(ma.Schema):
    name = fields.Str(required=True)
    email = fields.Str(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("name", "email")
        ordered = True


user_form_schema = UserFormSchema()
user_schema = UserSchema()
