from backend import ma
from marshmallow import fields


# This schema is used to validate the card form data
class StepFormSchema(ma.ModelSchema):
    name = fields.Str(required=True)
    md_content = fields.Str(required=True)
    code_snippet = fields.Str(required=False)
    image = fields.Str(required=False)
    github_raw_data = fields.Str(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("name", "md_content", "code_snippet", "image", "github_raw_data")
        ordered = True


# This schema is used to display step data
class StepSchema(ma.ModelSchema):
    id = fields.Int(required=False)
    name = fields.Str(required=True)
    md_content = fields.Str(required=True)
    code_snippet = fields.Str(required=False)
    image = fields.Str(required=False)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "name", "md_content", "code_snippet", "image")
        ordered = True


step_form_schema = StepFormSchema()
step_schema = StepSchema()
