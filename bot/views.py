from Chessnut import Game
from rest_framework.decorators import api_view
from rest_framework.response import Response
from bot.bot import Bot
from bot.models import BotResponse
from bot.serializers import BotResponseSerializer


@api_view(['POST'])
def play(request):
    if request.method != 'POST':
        return
    bot = Bot()
    board = request.data.get('board')
    if board is None:
        return

    game = Game(board)

    result_game = bot.make_best_move(1, game, True)
    serializer = BotResponseSerializer(BotResponse(board=result_game.get_fen, status=result_game.status))
    return Response(serializer.data)
