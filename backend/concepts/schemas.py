from backend import ma
from backend.steps.schemas import StepSchema
from marshmallow import fields


# This schema is used to validate concept form data
class ConceptFormSchema(ma.ModelSchema):
    name = fields.Str(required=True)
    cards = fields.List(fields.Int(), required=True)
    steps = fields.List(fields.Field, many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("name", "cards", "steps")
        ordered = True


# This schema is used to keep track
class ConceptSchema(ma.ModelSchema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    cards = fields.Nested("CardSchema", only=("id",), many=True)
    steps = fields.Nested(StepSchema, many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "name", "cards", "steps")
        ordered = True


concept_schema = ConceptSchema()
concept_form_schema = ConceptFormSchema()
