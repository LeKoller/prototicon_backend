from rest_framework import serializers

from .models import Content
from accounts.models import User


class ContentSerializer(serializers.Serializer):
    title = serializers.CharField()
    text = serializers.CharField(required=False)
    image = serializers.CharField(required=False)
    likes = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)
