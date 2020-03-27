from backend import ma
from marshmallow import fields


# This schema is used to validate the activity form data
class ActivityFormSchema(ma.Schema):
    github_id = fields.Int(required=True)
    filename = fields.Str(required=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    summary = fields.Str(required=True)
    difficulty = fields.Str(required=True)
    image = fields.Str(required=True)
    image_folder = fields.Str(required=False)
    cards = fields.Dict(required=True)

    class Meta:
        # Fields to show when sending data
        fields = (
            "github_id", "filename", "name", "description", "summary", "difficulty", "image", "image_folder",
            "cards")
        ordered = True


# This schema is used to display data in the Activity model
class ActivitySchema(ma.Schema):
    id = fields.Int(required=True)
    content_url = fields.Str(required=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    summary = fields.Str(required=True)
    is_project = fields.Bool(required=True)
    image = fields.Str(required=True)
    # We are referencing another Schema below. You do this in oder to avoid circular referencing
    cards = fields.Nested("CardSchema", only=("id", "content_url"), many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "content_url", "name", "description", "summary", "is_project", "image", "cards")
        ordered = True


# This schema is used to display data for all activities
class ActivitiesSchema(ma.ModelSchema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    difficulty = fields.Str(required=True)
    cards = fields.Nested("CardSchema", only=("name",), many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "name", "description", "difficulty", "cards")
        ordered = True


activity_form_schema = ActivityFormSchema()
activity_schema = ActivitySchema()
activities_schema = ActivitiesSchema(many=True)
