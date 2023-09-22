from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from rest_framework import serializers
from api.models import Game, GameMember

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'id']


class GameMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = GameMember
        fields = ['id', 'user', 'is_winner', ]


class GameSerializer(serializers.ModelSerializer):
    white = GameMemberSerializer(many=False, read_only=True)
    black = GameMemberSerializer(many=False, read_only=True)

    class Meta:
        model = Game
        fields = '__all__'

    @sync_to_async
    def get_data(self):
        return self.data
