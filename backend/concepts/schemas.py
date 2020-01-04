from backend import ma
from marshmallow import fields


# This schema is used to keep track
class ConceptSchema(ma.ModelSchema):
    id = fields.Int(required=True)
    contentful_id = fields.Str(required=True)
    name = fields.Str(required=True)
    steps = fields.Nested("StepSchema", only=("id", "contentful_id"), many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "contentful_id", "name", "steps")
        ordered = True


concept_schema = ConceptSchema()
