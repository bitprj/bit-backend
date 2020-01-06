from backend import ma
from marshmallow import fields


# This schema is used to keep track of checkpoint data
class CheckpointProgressSchema(ma.ModelSchema):
    checkpoint_id = fields.Int(required=True)
    contentful_id = fields.Str(required=True)
    is_completed = fields.Boolean(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("checkpoint_id", "contentful_id", "is_completed")
        ordered = True


checkpoint_progress_schema = CheckpointProgressSchema()
