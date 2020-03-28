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
    concepts = fields.List(fields.Int(), required=False)

    class Meta:
        # Fields to show when sending data
        fields = ("name", "order", "gems", "filename", "activity_filename", "github_raw_data", "concepts")
        ordered = True


# This schema is used to keep track of card data
class CardSchema(ma.ModelSchema):
    id = fields.Int(required=True)
    content_url = fields.Str(required=True)
    activity_id = fields.Int(required=True)
    content = fields.Str(required=True)
    gems = fields.Int(required=True)
    name = fields.Str(required=True)
    # activity is used to keep track of which activity that the card belongs to
    concepts = ma.Nested("ConceptSchema", only=("id", "content_url"), many=True)
    hints = ma.Nested("HintSchema", only=("id", "content_url", "hints"), many=True)
    checkpoint = ma.Nested("CheckpointSchema", only=("id", "content_url"))

    class Meta:
        # Fields to show when sending data
        fields = ("id", "content_url", "activity_id", "content", "gems", "name", "concepts", "hints", "checkpoint")
        ordered = True


card_form_schema = CardFormSchema()
card_schema = CardSchema()
