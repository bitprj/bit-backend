from backend import ma
from marshmallow import fields


# This schema is used to validate the checkpoint form data
class CheckpointFormSchema(ma.Schema):
    name = fields.Str(required=True)
    checkpoint_type = fields.Str(required=True)
    instruction = fields.Str(required=True)
    filename = fields.Str(required=True)
    mc_choices = fields.Dict(required=False)

    class Meta:
        # Fields to show when sending data
        fields = ("name", "checkpoint_type", "instruction", "filename", "mc_choices")
        ordered = True


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


checkpoint_form_schema = CheckpointFormSchema()
checkpoint_schema = CheckpointSchema()
