from backend import ma
from marshmallow import fields


# This schema is used to keep track of checkpoint data
class CheckpointSchema(ma.ModelSchema):
    id = fields.Int(required=True)
    contentful_id = fields.Str(required=True)
    name = fields.Str(required=True)
    checkpoint_type = fields.Str(required=True)
    mc_question = fields.Nested("MCQuestionSchema", required=False, many=False)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "contentful_id", "name", "checkpoint_type", "mc_question")
        ordered = True


checkpoint_schema = CheckpointSchema()
