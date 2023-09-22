import time

from asgiref.sync import sync_to_async
from celery import shared_task
from channels.layers import get_channel_layer

from api import serializers
from api.models import Game, GameStatus

channel_layer = get_channel_layer()


@shared_task
def realtime_timer_broadcast(session: Game):
    timer = 0
    while True:
        timer -= 1
        time.sleep(1)


@shared_task
def end_game_out_of_time(session: Game):
    winner = session.black if session.is_white_turn else session.white
    serializer = await sync_to_async(serializers.GameSerializer)(session)
    await session.end(GameStatus.OUT_OF_TIME, winner=winner)

    return await channel_layer.group_send(
        str(session.id), {
            'type': 'handle_end_game',
            'result_data': await serializer.get_data()
        }
    )
