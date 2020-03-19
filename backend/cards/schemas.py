from backend import ma
from marshmallow import fields


# This schema is used to validate the card form data
class CardFormSchema(ma.ModelSchema):
    name = fields.Str(required=True)
    order = fields.Int(required=True)
    gems = fields.Int(required=True)
    filename = fields.Str(required=True)
    activity_filename = fields.Str(required=True)
    github_raw_data = fields.Str(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("name", "order", "gems", "filename", "activity_filename", "github_raw_data")
        ordered = True


# This schema is used to keep track of card data
class CardSchema(ma.ModelSchema):
    id = fields.Int(required=True)
    contentful_id = fields.Str(required=True)
    name = fields.Str(required=True)
    order = fields.Int(required=True)
    # activity is used to keep track of which activity that the card belongs to
    activity = ma.Nested("ActivitySchema", only=("id", "contentful_id"))
    concepts = ma.Nested("ConceptSchema", only=("id", "contentful_id"), many=True)
    hints = ma.Nested("HintSchema", only=("id", "contentful_id", "order", "hints"), many=True)
    checkpoint = ma.Nested("CheckpointSchema", only=("id", "contentful_id"))

    class Meta:
        # Fields to show when sending data
        fields = ("id", "contentful_id", "name", "order", "activity", "concepts", "hints", "checkpoint")
        ordered = True


card_form_schema = CardFormSchema()
card_schema = CardSchema()
