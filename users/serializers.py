from rest_framework import serializers

from users.models import User, FriendRequest


class UserPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'profile_img_url', ]


class FriendRequestSerializer(serializers.ModelSerializer):
    sender = UserPreviewSerializer(many=False, read_only=True)
    receiver = UserPreviewSerializer(many=False, read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', ]
