from backend import ma
from marshmallow import fields


# This schema is used to validate step data
class StepFormSchema(ma.ModelSchema):
    heading = fields.Str(required=True)
    content = fields.Str(required=True)
    order = fields.Int(required=True)
    image = fields.Str(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("heading", "content", "order", "image")
        ordered = True


# This schema is used to display step data
class StepSchema(ma.ModelSchema):
    id = fields.Int(required=False)
    heading = fields.Str(required=True)
    content = fields.Str(required=True)
    order = fields.Int(required=True)
    image = fields.Str(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "heading", "content", "order", "image")
        ordered = True


step_form_schema = StepFormSchema()
step_schema = StepSchema()
