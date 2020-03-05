from backend import ma
from marshmallow import fields


# This schema is used to keep track
class CardSchema(ma.ModelSchema):
    id = fields.Int(required=True)
    contentful_id = fields.Str(required=True)
    name = fields.Str(required=True)
    order = fields.Int(required=True)
    # activity is used to keep track of which activity that the card belongs to
    activity = ma.Nested("ActivitySchema", only=("id", "contentful_id"))
    concepts = ma.Nested("ConceptSchema", only=("id", "contentful_id"), many=True)
    hints = ma.Nested("HintSchema", only=("id", "contentful_id", "hints"), many=True)
    checkpoint = ma.Nested("CheckpointSchema", only=("id", "contentful_id"))

    class Meta:
        # Fields to show when sending data
        fields = ("id", "contentful_id", "name", "order", "activity", "concepts", "hints", "checkpoint")
        ordered = True


card_schema = CardSchema()
