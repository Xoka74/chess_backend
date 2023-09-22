import uuid
from random import Random
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class GameStatus(models.IntegerChoices):
    STARTED = 0
    CHECK = 1
    CHECKMATE = 2
    STALEMATE = 3
    SURRENDER = 4
    OUT_OF_TIME = 5


class GameMember(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='members')
    is_winner = models.BooleanField(default=False)
    remaining_time_milliseconds = models.BigIntegerField()


class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_datetime = models.DateTimeField(default=timezone.now)
    end_datetime = models.DateTimeField(null=True)
    board = models.CharField(max_length=100, default='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    status = models.IntegerField(choices=GameStatus.choices, default=0)

    white = models.OneToOneField(GameMember, on_delete=models.CASCADE, related_name='game_1', null=True)
    black = models.OneToOneField(GameMember, on_delete=models.CASCADE, related_name='game_2', null=True)

    @staticmethod
    async def acreate(first_id, second_id, minutes_duration):
        random = Random()
        game = await Game.objects.acreate(status=GameStatus.STARTED)
        random_color = random.randint(0, 1)

        remaining_time = minutes_duration * 1000

        if random_color == 0:
            game.white = await GameMember.objects.acreate(user_id=first_id, remaining_time_milliseconds=remaining_time)
            game.black = await GameMember.objects.acreate(user_id=second_id, remaining_time_milliseconds=remaining_time)
        else:
            game.white = await GameMember.objects.acreate(user_id=second_id, remaining_time_milliseconds=remaining_time)
            game.black = await GameMember.objects.acreate(user_id=first_id, remaining_time_milliseconds=remaining_time)

        await game.asave()

        return game

    @database_sync_to_async
    def awhite(self):
        return self.white

    @database_sync_to_async
    def ablack(self):
        return self.black

    @property
    def winner(self):
        if self.white.is_winner:
            return self.white
        elif self.black.is_winner:
            return self.black

        return None

    @property
    def is_finished(self):
        return self.status > GameStatus.CHECK

    @property
    def current_turn_color(self):
        return self.board.split(' ')[1]

    @property
    def is_white_turn(self):
        return self.current_turn_color == 'w'

    @database_sync_to_async
    def aget_member(self, user_id):
        if self.white.user_id == user_id:
            return self.white
        elif self.black.user_id == user_id:
            return self.black

        return None

    @database_sync_to_async
    def end(self, status, winner=None):
        self.end_datetime = timezone.now()
        self.status = status
        if winner:
            winner.is_winner = True
            winner.save()
        self.save()
