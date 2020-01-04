from backend import ma
from marshmallow import fields


# This schema is used to display ActivityProgress data
class ActivityProgressSchema(ma.ModelSchema):
    last_card_completed = fields.Int(required=True)
    cards_locked = fields.Nested("CardSchema", only=("id", "name", "order"), many=True)
    cards_unlocked = fields.Nested("CardSchema", only=("id", "name", "order"), many=True)

    class Meta:
        # Fields to show when sending data
        fields = ("last_card_completed", "cards_locked", "cards_unlocked")
        ordered = True


class ActivityProgressVideo(ma.ModelSchema):
    video = fields.Str(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("video",)


activity_progress_schema = ActivityProgressSchema()
activity_progress_video = ActivityProgressVideo()
