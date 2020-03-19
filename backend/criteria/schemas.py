from backend import ma
from marshmallow import fields


# This schema is used to validate the criteria form data
class CriteriaFormSchema(ma.Schema):
    content = fields.Str(required=True)
    criteria_key = fields.Str(required=True)
    checkpoint_id = fields.Int(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("content", "criteria_key", "checkpoint_id")
        ordered = True


criteria_form_schema = CriteriaFormSchema()
