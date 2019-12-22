from backend import ma
from backend.steps.schemas import StepSchema
from marshmallow import fields


# This schema is used to validate hint form data
class HintFormSchema(ma.ModelSchema):
    name = fields.Str(required=True)
    difficulty = fields.Str(required=True)
    gems = fields.Int(required=True)
    parent = fields.Int(missing=None, required=False)
    steps = fields.List(fields.Field, many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("name", "difficulty", "gems", "parent ", "steps")
        ordered = True


# This schema is used to keep track
class HintSchema(ma.ModelSchema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    difficulty = fields.Str(required=True)
    gems = fields.Int(required=True)
    parent = fields.Int(missing=None, required=False)
    steps = fields.Nested(StepSchema, many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "name", "difficulty", "gems", "parent", "steps")
        ordered = True


hint_schema = HintSchema()
hint_form_schema = HintFormSchema()
