import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from api.models import Game
from matchmaking.models import UserIntent


class MatchmakingConsumer(AsyncJsonWebsocketConsumer):

    @property
    def user(self):
        return self.scope['user']

    async def connect(self):
        if not self.user.is_authenticated:
            return

        await self.accept()

        intents = UserIntent.objects.aiterator()

        async for intent in intents:
            intent_id = str(intent.id)
            await intent.adelete()
            intent_user = await intent.auser()

            session = await Game.acreate(intent_user.id, self.user.id, 5000)

            await self.channel_layer.group_add(intent_id, self.channel_name)

            return await self.channel_layer.group_send(intent_id, {
                'type': 'handle_match_found',
                'result_data': {
                    'session_id': str(session.id),
                }
            })

        intent = await UserIntent.objects.acreate(user=self.user)
        intent.asave()

        await self.channel_layer.group_add(str(intent.id), self.channel_name)

    async def handle_match_found(self, event):
        data = event['result_data']
        return await self.send(json.dumps({
            'type': 'match_found',
            'result_data': data
        }))

    async def disconnect(self, code):
        try:
            intent = await UserIntent.objects.aget(user=self.user)
            await intent.adelete()
        except (UserIntent.DoesNotExist, UserIntent.DoesNotExist):
            pass
