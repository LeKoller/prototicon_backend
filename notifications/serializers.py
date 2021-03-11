from rest_framework import serializers


class NotificationSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    of_type = serializers.CharField()
    message = serializers.CharField()
    is_seen = serializers.BooleanField(required=False)
    user_username = serializers.CharField()
    user_id = serializers.IntegerField(write_only=True, required=False)


class NotificationsListSerializer(serializers.Serializer):
    notifications = NotificationSerializer(many=True)
