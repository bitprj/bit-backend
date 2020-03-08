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
    hints = fields.Nested("HintSchema", only=("id", "contentful_id"), many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "contentful_id", "name", "parent", "steps", "hints")
        ordered = True


class HintStatusSchema(ma.ModelSchema):
    hint = fields.Nested("HintSchema", only=("id", "contentful_id"), many=False, required=True)
    hints = fields.Nested("HintStatusSchema", only=("is_unlocked", "hints"), many=True)
    is_unlocked = fields.Boolean(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("hint", "hints", "is_unlocked")
        ordered = True


hint_schema = HintSchema()
hint_status_schemas = HintStatusSchema(many=True)
