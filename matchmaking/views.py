from django.shortcuts import render


def matchmaking(request):
    return render(request, 'matchmaking/index.html')
