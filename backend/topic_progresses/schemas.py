from backend import ma
from marshmallow import fields


# This schema is used to display the students topic progress
class TopicProgressSchema(ma.ModelSchema):
    completed_modules = fields.Nested("ModuleSchema", only=("id", "name"), many=True)
    incomplete_modules = fields.Nested("ModuleSchema", only=("id", "name"), many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("completed_modules", "incomplete_modules")
        ordered = True


topic_progress_schema = TopicProgressSchema()
