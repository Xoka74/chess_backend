from django.urls import path

from bot import views

urlpatterns = [
    path('play/', views.play, name='bot-play')
]
