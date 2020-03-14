from backend import ma
from marshmallow import fields


# This schema is used to validate multiple choice form data
class MCChoiceFormSchema(ma.Schema):
    content = fields.Str(required=True)
    checkpoint_id = fields.Int(required=True)
    mc_choice_key = fields.Str(required=True)
    is_correct_choice = fields.Bool(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("content", "checkpoint_id", "mc_choice_key", "is_correct_answer")
        ordered = True


# This schema is used to keep track of the Multiple Choice data
class MCChoiceSchema(ma.ModelSchema):
    id = fields.Int(required=True)
    contentful_id = fields.Str(required=True)
    name = fields.Str(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "contentful_id", "name")
        ordered = True


mc_choice_form_schema = MCChoiceFormSchema()
mc_choice_schema = MCChoiceSchema()
