from backend import ma
from marshmallow import fields


# This schema is used to validate the badge form data
class OrganizationFormSchema(ma.Schema):
    name = fields.Str(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("name",)
        ordered = True


# This schema validates the files in the form
class OrganizationFileSchema(ma.Schema):
    image = fields.Field(required=True)
    background_image = fields.Field(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("image", "background_image")
        ordered = True


# This schema is used to display the organization data
class OrganizationSchema(ma.Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    image = fields.Str(required=True)
    background_image = fields.Str(required=True)
    owners = fields.Nested("UserSchema", only=("email",), many=True)
    active_users = fields.Nested("UserSchema", only=("email",), many=True)
    inactive_users = fields.Nested("UserSchema", only=("email",), many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "name", "image", "background_image", "owners", "active_users", "inactive_users")
        ordered = True


organization_form_schema = OrganizationFormSchema()
organization_file_schema = OrganizationFileSchema()
organization_schema = OrganizationSchema()
