from backend import ma
from marshmallow import fields


# This schema is used to keep track
class CardSchema(ma.ModelSchema):
    id = fields.Int(required=True)
    contentful_id = fields.Str(required=True)
    name = fields.Str(required=True)
    # activity is used to keep track of which activity that the card belongs to
    activity = ma.Nested("ActivitySchema", only=("id", "contentful_id"))
    concepts = ma.Nested("ConceptSchema", only=("id",), many=True)
    hints = ma.Nested("HintSchema", only=("id",), many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "contentful_id", "name", "activity", "concepts", "hints")
        ordered = True


card_schema = CardSchema()
