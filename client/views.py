from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from api.models import Game, GameStatus


@login_required
def home(request):
    return render(request, 'client/home.html')


@login_required
def history(request):
    games = Game.objects.filter(members__user_id=request.user.id, status__gt=GameStatus.CHECK)
    return render(request, 'client/history.html', {'sessions': games})


@login_required
def session(request, id):
    game = get_object_or_404(Game, id=id)
    member = game.aget_member(request.user.id)
    if member:
        return render(request, 'client/game.html', {'session': game, 'member': member})

    return Http404()


@login_required
def delete_session(request, id):
    game = Game.objects.get(id=id)
    game.delete()
    return redirect('client-history')
