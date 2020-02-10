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
    name = fields.Str(required=True)
    image = fields.Str(required=True)
    background_image = fields.Str(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("name", "image", "background_image")
        ordered = True


organization_form_schema = OrganizationFormSchema()
organization_file_schema = OrganizationFileSchema()
organization_schema = OrganizationSchema()
