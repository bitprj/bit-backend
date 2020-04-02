from marshmallow import fields
from backend import ma


# This schema is used to display student data
class StudentSchema(ma.Schema):
    id = fields.Str(required=True)
    name = fields.Str(required=True)
    last_seen = fields.DateTime(required=False)
    suggested_activity = fields.Nested("ActivitySchema", only=("id",), many=False)
    current_activities = fields.Nested("ActivitySchema", only=("id", "content_url"), many=True)
    inprogress_modules = fields.Nested("ModuleSchema", only=("id", "name"), many=True)
    inprogress_topics = fields.Nested("TopicSchema", only=("id", "name"), many=True)

    class Meta:
        # Fields to show when sending data
        fields = (
            "id", "name", "last_seen", "suggested_activity", "current_activities", "inprogress_modules",
            "inprogress_topics")
        ordered = True


# This schema is used to display data based on the classroom that they are in
class StudentClassroomSchema(ma.ModelSchema):
    classes = fields.Nested("ClassroomSchema", only=("id", "modules"), many=True)
    inprogress_modules = fields.Nested("ModuleSchema", only=("id",), many=True)
    completed_activities = fields.Nested("ActivitySchema", only=("id",), many=True)
    current_activities = fields.Nested("ActivitySchema", only=("id",), many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("classes", "inprogress_modules", "completed_activities")
        ordered = True


# This schema is used to validate the data sent for UpdateStudentData
class UpdateDataSchema(ma.Schema):
    module_id = fields.Int(required=True)

    class Meta:
        fields = ("module_id",)
        ordered = True


student_schema = StudentSchema()
student_classroom_schema = StudentClassroomSchema()
update_data_schema = UpdateDataSchema()
