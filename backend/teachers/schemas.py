from backend import ma
from marshmallow import fields


# This schema is used to display the classroom data
class TeacherClassroomSchema(ma.ModelSchema):
    classrooms = fields.Nested("ClassroomSchema", only=("id",), many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("classrooms",)
        ordered = True


teacher_classroom_schema = TeacherClassroomSchema()
