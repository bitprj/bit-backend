from backend import ma
from marshmallow import fields


# This schema is used to validate card form data
class CardFormSchema(ma.ModelSchema):
    name = fields.Str(required=True)
    md_file = fields.Str(required=True)
    order = fields.Int(required=True)
    gems = fields.Int(required=True)
    concepts = fields.List(fields.Int(), required=False)

    class Meta:
        # Fields to show when sending data
        fields = ("name", "md_file", "order", "gems", "concepts")
        ordered = True


# This schema is used to keep track
class CardSchema(ma.ModelSchema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    md_file = fields.Str(required=True)
    order = fields.Int(required=True)
    gems = fields.Int(required=True)
    # activity is used to keep track of which activity that the card belongs to
    activity = ma.Nested("ActivitySchema", only=("id",))
    concepts = ma.Nested("ConceptSchema", only=("id",), many=True)
    hints = ma.Nested("HintSchema", only=("id",), many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "name", "md_file", "order", "gems", "activity", "concepts", "hints")
        ordered = True


card_schema = CardSchema()
card_form_schema = CardFormSchema()
