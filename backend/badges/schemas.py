from backend import ma
from marshmallow import fields


# This schema is used to validate the badge form data
class BadgeSchema(ma.Schema):
    name = fields.Str(required=True)
    contentful_id = fields.Str(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "contentful_id", "name")
        ordered = True


# This schema is used to display data in any badge association object
class BadgeRequirementSchema(ma.ModelSchema):
    badge_id = fields.Int(required=False)
    xp = fields.Int(required=False)


# This schema is used to display the data in a module's badge_weights
class ModuleBadgeWeightSchema(ma.ModelSchema):
    badge_id = fields.Int(required=True)
    weight = fields.Float(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("id", "badge_id", "weight")
        ordered = True


badge_schema = BadgeSchema()
badges_schema = BadgeSchema(many=True)
