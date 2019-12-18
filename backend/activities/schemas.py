from backend import ma
from marshmallow import fields


class ActivitySchema(ma.Schema):
    name = fields.String(required=True)
    description = fields.String(required=True)
    summary = fields.String(required=True)
    difficulty = fields.String(required=True)
    image = fields.Field(required=False)
    badge_prereqs = fields.List(fields.Dict(), required=False)
    # module_ids are the list of module_ids that keep track of which modules own this lab
    module_ids = fields.List(fields.Int(), required=False)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "name", "description", "summary", "difficulty", "image", "badge_prereqs", "module_ids")
        ordered = True


activity_schema = ActivitySchema()
