from rest_framework import serializers

from .models import User
from notifications.serializers import NotificationSerializer


class FollowerSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    image = serializers.ImageField(read_only=True)


class ContentIDSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        instance = User.objects.create_user(**validated_data)
        return instance

    password = serializers.CharField(write_only=True)
    is_staff = serializers.BooleanField(default=False)
    is_superuser = serializers.BooleanField(default=False)
    image = serializers.ImageField(read_only=True)
    wallpaper = serializers.ImageField(read_only=True)
    following = FollowerSerializer(many=True, read_only=True)
    followers = FollowerSerializer(many=True, read_only=True)
    liked_content = ContentIDSerializer(many=True, read_only=True)


class UserImageSerializer(serializers.Serializer):
    image = serializers.ImageField()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class EditUserSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True, required=False)
    is_staff = serializers.BooleanField(default=False, required=False)
    is_superuser = serializers.BooleanField(default=False, required=False)


class FriendsSerializer(serializers.Serializer):
    friends = UserSerializer(many=True)
