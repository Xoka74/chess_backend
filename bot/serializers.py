from rest_framework import serializers


class BotResponseSerializer(serializers.Serializer):
    board = serializers.CharField(max_length=100)
    status = serializers.IntegerField()
