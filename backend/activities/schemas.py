from backend import ma
from marshmallow import fields


# This schema is used to display data in the Activity model
class ActivitySchema(ma.Schema):
    id = fields.Int(required=True)
    contentful_id = fields.Str(required=True)
    name = fields.Str(required=True)
    # We are referencing another Schema below. You do this in oder to avoid circular referencing
    cards = fields.Nested("CardSchema", only=("id", "contentful_id", "name", "order"), many=True)
    checkpoints = fields.Nested("CheckpointSchema", only=("id", "contentful_id"), many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "contentful_id", "name", "cards", "checkpoints")
        ordered = True


activity_schema = ActivitySchema()
activities_schema = ActivitySchema(many=True)
