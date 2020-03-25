from backend import ma
from marshmallow import fields


# This schema is used to validate the checkpoint form data
class CheckpointFormSchema(ma.Schema):
    name = fields.Str(required=True)
    cards_folder = fields.Str(required=True)
    checkpoint_type = fields.Str(required=True)
    instruction = fields.Str(required=True)
    filename = fields.Str(required=True)
    image = fields.Str(required=False)
    image_folder = fields.Str(required=False)
    files_to_send = fields.Str(required=False)
    test_file_location = fields.Str(required=False)
    mc_choices = fields.Dict(required=False)
    criteria = fields.Dict(required=False)
    correct_choice = fields.Str(required=False)

    class Meta:
        # Fields to show when sending data
        fields = (
            "name", "cards_folder", "checkpoint_type", "instruction", "filename", "image", "image_folder",
            "files_to_send", "test_file_location", "mc_choices", "criteria", "correct_choice")
        ordered = True


# This schema is used to keep track of checkpoint data
class CheckpointSchema(ma.ModelSchema):
    id = fields.Int(required=True)
    contentful_id = fields.Str(required=True)
    instruction = fields.Str(required=True)
    name = fields.Str(required=True)
    checkpoint_type = fields.Str(required=True)
    criteria = fields.Nested("CriteriaSchema", required=False, many=True)
    choices = fields.Nested("MCChoiceSchema", required=False, many=True)
    correct_choice = fields.Nested("MCChoiceSchema", required=False, many=False)

    class Meta:
        # Fields to show when sending data
        fields = (
            "id", "contentful_id", "instruction", "name", "checkpoint_type", "criteria", "choices", "correct_choice")
        ordered = True


# This schema is used to keep track of criteria data for checkpoints
class CriteriaSchema(ma.ModelSchema):
    content = fields.Str(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("content",)
        ordered = True


checkpoint_form_schema = CheckpointFormSchema()
checkpoint_schema = CheckpointSchema()
