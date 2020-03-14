from backend import ma
from marshmallow import fields


# This schema is used to validate the checkpoint form data
class CheckpointFormSchema(ma.Schema):
    name = fields.Str(required=True)
    checkpoint_type = fields.Str(required=True)
    instruction = fields.Str(required=True)
    filename = fields.Str(required=True)
    mc_choices = fields.Dict(required=False)
    correct_choice = fields.Str(required=False)

    class Meta:
        # Fields to show when sending data
        fields = ("name", "checkpoint_type", "instruction", "filename", "mc_choices", "correct_choice")
        ordered = True


# This schema is used to keep track of checkpoint data
class CheckpointSchema(ma.ModelSchema):
    id = fields.Int(required=True)
    contentful_id = fields.Str(required=True)
    name = fields.Str(required=True)
    checkpoint_type = fields.Str(required=True)
    choices = fields.Nested("MCChoiceSchema", required=False, many=True)
    correct_choice = fields.Nested("MCChoiceSchema", required=False, many=False)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "contentful_id", "name", "checkpoint_type", "choices", "correct_choice")
        ordered = True


checkpoint_form_schema = CheckpointFormSchema()
checkpoint_schema = CheckpointSchema()
