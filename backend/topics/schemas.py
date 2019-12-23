from backend import ma
from marshmallow import fields


# This schema is used to validate topic form data
class TopicFormSchema(ma.ModelSchema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    modules = fields.List(fields.Int(), required=False)
    activity_prereqs = fields.List(fields.Int(), required=False)
    module_prereqs = fields.List(fields.Int(), required=False)
    badge_prereqs = fields.List(fields.Dict(), required=False)

    class Meta:
        # Fields to show when sending data
        fields = ("name", "description", "modules", "activity_prereqs", "module_prereqs", "badge_prereqs")
        ordered = True


# This schema is used to keep track
class TopicSchema(ma.ModelSchema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    # We are referencing another Schema below. You do this in oder to avoid circular referencing
    # The only keyword is used to show the id of modules and badge requirements
    activity_prereqs = fields.Nested("ActivitySchema", only=("id",), many=True)
    badge_prereqs = fields.Nested("BadgeRequirementSchema", many=True)
    modules = ma.Nested("ModuleSchema", only=("id",), many=True)
    module_prereqs = ma.Nested("ModuleSchema", only=("id",), many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "name", "description", "activity_prereqs", "badge_prereqs", "modules", "module_prereqs")
        ordered = True


# This schema is used to display the students topic progress
class TopicProgressSchema(ma.ModelSchema):
    completed_modules = fields.Nested("ModuleSchema", only=("id", "name", "description", "icon"), many=True)
    incomplete_modules = fields.Nested("ModuleSchema", only=("id", "name", "description", "icon"), many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("completed_modules", "incomplete_modules")
        ordered = True


topic_schema = TopicSchema()
topic_form_schema = TopicFormSchema()
topic_progress_schema = TopicProgressSchema()
