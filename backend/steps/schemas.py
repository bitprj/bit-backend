from backend import ma
from marshmallow import fields


# This schema is used to display step data
class StepSchema(ma.ModelSchema):
    id = fields.Int(required=False)
    contentful_id = fields.Str(required=True)
    heading = fields.Str(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "contentful_id", "heading")
        ordered = True


step_schema = StepSchema()
