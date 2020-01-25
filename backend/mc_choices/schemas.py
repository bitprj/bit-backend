from backend import ma
from marshmallow import fields


# This schema is used to keep track
class MCChoiceSchema(ma.ModelSchema):
    id = fields.Int(required=True)
    contentful_id = fields.Str(required=True)
    name = fields.Str(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "contentful_id", "name")
        ordered = True


mc_choice_schema = MCChoiceSchema()
