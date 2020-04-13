from serpy import IntField, MethodField, Serializer, StrField


# This schema is used to display user data,
class UserSerializer(Serializer):
    name = StrField(required=True)
    email = StrField(required=True)
    github_username = StrField(required=True)
    image = StrField(required=True)
    global_gems = IntField(required=True)
    last_seen = MethodField("serialize_last_seen")

    def serialize_last_seen(self, user):
        if not user.last_seen:
            return None
        return user.last_seen.isoformat()
