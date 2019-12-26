from backend import ma
from marshmallow import fields


# This schema is used to display student data
class StudentSchema(ma.Schema):
    name = fields.Str(required=True)
    current_activities = fields.Nested("ActivitySchema", only=("id", ), many=True)
    current_topic_id = fields.Int(required=True)
    current_track_id = fields.Int(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("name", "current_activities", "current_topic_id", "current_track_id")
        ordered = True


student_schema = StudentSchema()
