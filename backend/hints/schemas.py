from backend import ma
from backend.steps.schemas import StepSchema
from marshmallow import fields


# This schema is used to keep track
class HintSchema(ma.ModelSchema):
    id = fields.Int(required=True)
    contentful_id = fields.Str(required=True)
    name = fields.Str(required=True)
    parent = fields.Int(missing=None, required=False)
    steps = fields.Nested(StepSchema, many=True)
    hint_children = fields.Nested("HintSchema", only=("id", "contentful_id"), many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "contentful_id", "name", "parent", "steps", "hint_children")
        ordered = True


hint_schema = HintSchema()
