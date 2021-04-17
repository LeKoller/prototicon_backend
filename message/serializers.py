from rest_framework import serializers

from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["author_username",
                  "target_username",
                  "text",
                  "read",
                  "in_reply_of_id"]

    read = serializers.BooleanField(read_only=True)
    in_reply_of_id = serializers.IntegerField(required=False)
    author_username = serializers.CharField(required=False)
