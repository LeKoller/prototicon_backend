from rest_framework import serializers

from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        exclude = ['author', 'target']

    id = serializers.IntegerField(read_only=True)
    read = serializers.BooleanField(read_only=True)
    author_username = serializers.CharField(required=False)
    in_reply_of = serializers.PrimaryKeyRelatedField(
        required=False, read_only=True)
