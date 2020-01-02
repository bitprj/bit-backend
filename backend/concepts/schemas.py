from backend import ma
from backend.steps.schemas import StepSchema
from marshmallow import fields


# This schema is used to keep track
class ConceptSchema(ma.ModelSchema):
    id = fields.Int(required=True)
    contentful_id = fields.Str(required=True)
    cards = fields.Nested("CardSchema", only=("id",), many=True)
    steps = fields.Nested(StepSchema, many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "contentful_id", "name", "cards", "steps")
        ordered = True


concept_schema = ConceptSchema()
