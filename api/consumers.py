import json

import Chessnut
from Chessnut.game import InvalidMove
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from api import serializers
from api.models import Game, GameStatus


class SessionConsumer(AsyncJsonWebsocketConsumer):
    @property
    def user(self):
        return self.scope['user']

    @property
    def game_id(self):
        return self.scope['url_route']['kwargs']['game_id']

    async def connect(self):
        game = await database_sync_to_async(Game.objects.get)(id=self.game_id)

        if game.is_finished:
            return

        member = await game.aget_member(self.user.id)
        if not member:
            return None

        serializer = await sync_to_async(serializers.GameSerializer)(game)

        await self.channel_layer.group_add(self.game_id, self.channel_name)
        await self.accept()
        await self.send(json.dumps({
            'type': 'join_game',
            'result_data': await serializer.get_data()
        }))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.game_id, self.channel_name)

    async def receive_json(self, json_data, **kwargs):
        print(json_data)
        event_type = json_data['event_type']
        data = json_data['event_data']
        game = await Game.objects.aget(id=self.game_id)
        if game.is_finished:
            return
        member = await game.aget_member(self.user.id)

        if event_type == "make_move":
            if (member == await game.awhite()) != game.is_white_turn:
                return

            chessnut_game = Chessnut.Game(fen=game.board)

            try:
                chessnut_game.apply_move(data['move'])
                game.board = chessnut_game.get_fen()

                if chessnut_game.status > Chessnut.Game.CHECK:
                    await game.end(chessnut_game.status, winner=member)
                    serializer = await sync_to_async(serializers.GameSerializer)(game)
                    return await self.channel_layer.group_send(
                        self.game_id, {
                            'type': 'handle_end_game',
                            'result_data': await serializer.get_data()
                        }
                    )

                await game.asave()
                serializer = await sync_to_async(serializers.GameSerializer)(game)
                await self.channel_layer.group_send(
                    self.game_id, {
                        'type': f'handle_make_move',
                        'result_data': await serializer.get_data()
                    }
                )
            except InvalidMove:
                return
        elif event_type == "surrender":
            white = await game.awhite()
            other_member = await game.ablack() if (member == white) else white

            await game.end(GameStatus.SURRENDER, winner=other_member)
            serializer = await sync_to_async(serializers.GameSerializer)(game)
            await game.asave()
            return await self.channel_layer.group_send(
                self.game_id, {
                    'type': 'handle_end_game',
                    'result_data': await serializer.get_data()
                }
            )

    async def handle_end_game(self, event):
        await self.send(json.dumps({
            'type': 'end_game',
            'result_data': event['result_data']
        }))

    async def handle_make_move(self, event):
        await self.send(json.dumps({
            'type': 'make_move',
            'result_data': event['result_data']
        }))
