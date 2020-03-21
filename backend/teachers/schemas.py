<<<<<<< HEAD
from marshmallow import fields
from backend import ma


# This schema is used to display student data
class TeacherClassroomsSchema(ma.Schema):
=======
from backend import ma
from marshmallow import fields


# This schema is used to display the classroom data
class TeacherClassroomSchema(ma.ModelSchema):
>>>>>>> b3af5b20644906b7b92342efa680bd79a1145f13
    classrooms = fields.Nested("ClassroomSchema", only=("id",), many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("classrooms",)
        ordered = True


<<<<<<< HEAD
teacher_classroom_schema = TeacherClassroomsSchema()
=======
teacher_classroom_schema = TeacherClassroomSchema()
>>>>>>> b3af5b20644906b7b92342efa680bd79a1145f13
