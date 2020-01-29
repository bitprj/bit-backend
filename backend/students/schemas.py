from marshmallow import fields

from backend import ma


# This schema is used to display student data
class StudentSchema(ma.Schema):
    name = fields.Str(required=True)
    current_activities = fields.Nested("ActivitySchema", only=("id",), many=True)
    inprogress_modules = fields.Nested("ModuleSchema", only=("id", "name", "contentful_id"), many=True)
    inprogress_topics = fields.Nested("TopicSchema", only=("id", "name", "contentful_id"), many=True)
    current_topic = fields.Nested("TopicSchema", only=("id", "contentful_id"), many=False)
    current_track = fields.Nested("TrackSchema", only=("id", "contentful_id"), many=False)

    class Meta:
        # Fields to show when sending data
        fields = (
            "name", "current_activities", "inprogress_modules", "inprogress_topics", "current_topic",
            "current_track")
        ordered = True


student_schema = StudentSchema()
