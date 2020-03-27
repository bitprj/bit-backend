from backend import ma
from backend.steps.schemas import StepSchema
from marshmallow import fields


# This schema is used to validate the card form data
class HintFormSchema(ma.ModelSchema):
    name = fields.Str(required=True)
    gems = fields.Int(required=True)
    order = fields.Int(required=True)
    filename = fields.Str(required=True)
    parent_filename = fields.Str(required=True)
    is_card_hint = fields.Bool(required=True)
    github_raw_data = fields.Str(required=True)
    steps = fields.Dict(required=True)
    image_folder = fields.Str(required=False)

    class Meta:
        # Fields to show when sending data
        fields = ("name", "gems", "order", "filename", "parent_filename", "is_card_hint", "github_raw_data", "steps",
                  "image_folder")
        ordered = True


# This schema is used to keep track of hint data
class HintSchema(ma.ModelSchema):
    id = fields.Int(required=True)
    content_url = fields.Str(required=True)
    name = fields.Str(required=True)
    gems = fields.Int(required=True)
    order = fields.Int(required=True)
    parent = fields.Int(missing=None, required=False)
    steps = fields.Nested(StepSchema, many=True)
    hints = fields.Nested("HintSchema", only=("id", "hints"), many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "content_url", "name", "gems", "order", "parent", "steps", "hints")
        ordered = True


class HintStatusSchema(ma.ModelSchema):
    hint_id = fields.Int(required=True)
    is_unlocked = fields.Boolean(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("hint_id", "is_unlocked")
        ordered = True


hint_form_schema = HintFormSchema()
hint_schema = HintSchema()
hint_status_schema = HintStatusSchema()
