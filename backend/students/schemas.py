from marshmallow import fields
from backend import ma
from serpy import IntField, MethodField, Serializer
import backend.activities.schemas as activity_schemas
import backend.classrooms.schemas as class_schemas
import backend.modules.schemas as module_schemas


# Serpy schema for serialization
class StudentSerializer(Serializer):
    id = IntField(required=True)
    classes = MethodField("serialize_classes", attr="classrooms")
    current_activities = MethodField("serialize_current_activities")
    completed_modules = MethodField("serialize_completed_modules")
    inprogress_modules = MethodField("serialize_inprogress_modules")
    incomplete_modules = MethodField("serialize_incomplete_modules")

    def serialize_classes(self, student):
        if not student.classes:
            return []
        return class_schemas.ClassroomRelSerializer(student.classes, many=True).data

    def serialize_current_activities(self, student):
        if not student.current_activities:
            return []
        return activity_schemas.ActivityRelSerializer(student.current_activities, many=True).data

    def serialize_completed_modules(self, student):
        if not student.completed_modules:
            return []
        return module_schemas.ModuleRelSerializer(student.completed_modules, many=True).data

    def serialize_inprogress_modules(self, student):
        if not student.inprogress_modules:
            return []
        return module_schemas.ModuleRelSerializer(student.inprogress_modules, many=True).data

    def serialize_incomplete_modules(self, student):
        if not student.incomplete_modules:
            return []
        return module_schemas.ModuleRelSerializer(student.incomplete_modules, many=True).data


# Serpy schema for serialization for relationships
class StudentRelSerializer(Serializer):
    id = IntField(required=True)


# Serpy schema for serialization for Student Classroom data
class StudentClassroomSerializer(Serializer):
    classes = MethodField("serialize_classes", attr="classrooms")
    inprogress_modules = MethodField("serialize_inprogress_modules")
    completed_activities = MethodField("serialize_completed_activities")
    current_activities = MethodField("serialize_current_activities")

    def serialize_classes(self, student):
        if not student.classes:
            return []
        return class_schemas.ClassroomRelSerializer(student.classes, many=True).data

    def serialize_inprogress_modules(self, student):
        if not student.inprogress_modules:
            return []
        return module_schemas.ModuleRelSerializer(student.inprogress_modules, many=True).data

    def serialize_completed_activities(self, student):
        if not student.completed_activities:
            return []
        return activity_schemas.ActivityRelSerializer(student.completed_activities).data

    def serialize_current_activities(self, student):
        if not student.current_activities:
            return []
        return activity_schemas.ActivityRelSerializer(student.current_activities).data


# This schema is used to validate the data sent for UpdateStudentData
class UpdateDataSchema(ma.Schema):
    suggested_activity = fields.Nested("SuggestedActivitySchema", required=True)

    class Meta:
        fields = ("suggested_activity",)
        ordered = True


update_data_schema = UpdateDataSchema()
