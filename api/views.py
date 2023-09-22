from django.db.models import Q
from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from api import serializers
from api.models import Game, GameStatus


class HistoryViewSet(ReadOnlyModelViewSet):
    queryset = Game.objects.all()
    serializer_class = serializers.GameSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query = Q(white__user_id=self.request.user.id)
        query.add(Q(black__user_id=self.request.user.id), Q.OR)
        query.add(Q(status__gt=GameStatus.CHECK), Q.AND)
        return super().get_queryset().filter(query)


class PendingSessionRetrieveView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = Q(white__user_id=self.request.user.id)
        query.add(Q(black__user_id=self.request.user.id), Q.OR)
        query.add(Q(status__lt=GameStatus.CHECKMATE), Q.AND)
        session = get_object_or_404(Game.objects, query)
        serializer = serializers.GameSerializer(session)
        return Response(serializer.data)
