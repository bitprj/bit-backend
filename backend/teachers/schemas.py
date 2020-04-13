from backend.classrooms.schemas import ClassroomSerializer
from serpy import IntField, MethodField, Serializer


# This schema is used to display user data,
class TeacherSerializer(Serializer):
    id = IntField(required=True)
    classrooms = MethodField("serialize_classrooms")

    def serialize_classrooms(self, teacher):
        if not teacher.classrooms:
            return []
        return ClassroomSerializer(teacher.classrooms, many=True).data
