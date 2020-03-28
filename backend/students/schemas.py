from marshmallow import fields

from backend import ma


# This schema is used to display student data
class StudentSchema(ma.Schema):
    id = fields.Str(required=True)
    name = fields.Str(required=True)
    current_activities = fields.Nested("ActivitySchema", only=("id", "content_url"), many=True)
    inprogress_modules = fields.Nested("ModuleSchema", only=("id", "name"), many=True)
    inprogress_topics = fields.Nested("TopicSchema", only=("id", "name"), many=True)
    current_topic = fields.Nested("TopicSchema", only=("id",), many=False)
    current_track = fields.Nested("TrackSchema", only=("id",), many=False)

    class Meta:
        # Fields to show when sending data
        fields = (
            "id", "name", "current_activities", "inprogress_modules", "inprogress_topics", "current_topic",
            "current_track")
        ordered = True


student_schema = StudentSchema()
