from backend import ma
from marshmallow import fields


# This schema is used to validate the card form data
class StepFormSchema(ma.ModelSchema):
    name = fields.Str(required=True)
    md_content = fields.Str(required=False)
    step_key = fields.Str(required=True)
    type = fields.Str(required=True)
    concept_id = fields.Int(required=False)
    hint_id = fields.Int(required=False)
    code_snippet = fields.Str(required=False)
    image = fields.Str(required=False)
    image_folder = fields.Str(required=False)

    class Meta:
        # Fields to show when sending data
        fields = (
            "name", "md_content", "step_key", "type", "concept_id", "hint_id", "code_snippet", "image", "image_folder")
        ordered = True


# This schema is used to display step data
class StepSchema(ma.ModelSchema):
    id = fields.Int(required=False)
    contentful_id = fields.Str(required=True)
    name = fields.Str(required=True)
    md_content = fields.Str(required=True)
    code_snippet = fields.Str(required=False)
    image = fields.Str(required=False)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "contentful_id", "name", "md_content", "code_snippet", "image")
        ordered = True


step_form_schema = StepFormSchema()
step_schema = StepSchema()
