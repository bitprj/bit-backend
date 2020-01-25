from backend import ma
from marshmallow import fields


# This schema is used to keep track
class MCQuestionSchema(ma.ModelSchema):
    id = fields.Int(required=True)
    contentful_id = fields.Str(required=True)
    name = fields.Str(required=True)
    choices = fields.Nested("MCChoiceSchema", only=("id", "contentful_id"), many=True)
    correct_choice = fields.Nested("MCChoiceSchema", only=("id", "contentful_id"), many=False)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "contentful_id", "name", "choices", "correct_choice")
        ordered = True


mc_question_schema = MCQuestionSchema()
