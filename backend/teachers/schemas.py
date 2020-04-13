from backend import ma
from backend.classrooms.schemas import ClassroomSerializer
from marshmallow import fields
from serpy import MethodField, Serializer


# This schema is used to display user data,
class TeacherClassroomSerializer(Serializer):
    classrooms = MethodField("serialize_classrooms")

    def serialize_classrooms(self, teacher):
        if not teacher.classrooms:
            return []
        return ClassroomSerializer(teacher.classrooms, many=True).data


# This schema is used to display the classroom data
class TeacherClassroomSchema(ma.ModelSchema):
    classrooms = fields.Nested("ClassroomSchema", only=("id",), many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("classrooms",)
        ordered = True


teacher_classroom_schema = TeacherClassroomSchema()
