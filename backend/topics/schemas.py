from backend import ma
from marshmallow import fields


# This schema is used to validate form data
class TopicFormSchema(ma.Schema):
    github_id = fields.Int(required=True)
    name = fields.Str(required=True)
    filename = fields.Str(required=True)
    description = fields.Str(required=True)
    image = fields.Str(required=True)
    image_folder = fields.Str(required=True)
    modules = fields.List(fields.Int, required=False)

    class Meta:
        # Fields to show when sending data
        fields = ("github_id", "name", "filename", "description", "image", "image_folder", "modules")
        ordered = True


# This schema is used to keep track
class TopicSchema(ma.ModelSchema):
    id = fields.Int(required=True)
    content_url = fields.Str(required=True)
    github_id = fields.Int(required=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)

    # We are referencing another Schema below. You do this in oder to avoid circular referencing
    # The only keyword is used to show the id of modules and badge requirements
    # activity_prereqs = fields.Nested("ActivitySchema", only=("id", "contentful_id"), many=True)
    # badge_prereqs = fields.Nested("BadgeRequirementSchema", many=True)
    modules = ma.Nested("ModuleSchema", only=("id", "name"), many=True)
    # module_prereqs = ma.Nested("ModuleSchema", only=("id", "contentful_id"), many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "content_url", "github_id", "name", "description", "modules")
        ordered = True


topic_schema = TopicSchema()
topic_form_schema = TopicFormSchema()
