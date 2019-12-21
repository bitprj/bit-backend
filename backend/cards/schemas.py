from backend import ma
from marshmallow import fields


# This schema is used to validate card form data
class CardFormSchema(ma.ModelSchema):
    name = fields.Str(required=True)
    md_file = fields.Str(required=True)
    gems = fields.Int(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("name", "md_file", "gems")
        ordered = True


# This schema is used to keep track
class CardSchema(ma.ModelSchema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    md_file = fields.Str(required=True)
    gems = fields.Int(required=True)
    activity_id = fields.Int(required=True)
    activity = ma.Nested("ActivitySchema", only=("id",), many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "name", "md_file", "gems", "activity_id")
        ordered = True


card_schema = CardSchema()
card_form_schema = CardFormSchema()
