from marshmallow import fields
from backend import ma


# This schema is used to display student data
class TeacherClassroomsSchema(ma.Schema):
    classrooms = fields.Nested("ClassroomSchema", only=("id",), many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("classrooms",)
        ordered = True


teacher_classroom_schema = TeacherClassroomsSchema()
