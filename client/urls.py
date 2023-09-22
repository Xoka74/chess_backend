from django.urls import path
from client import views

urlpatterns = [
    path('home', views.home, name='client-home'),
    path('history', views.history, name='client-history'),
    path('sessions/<int:id>', views.session, name='client-session'),
    path('sessions/<int:id>/delete', views.delete_session, name='client-session-delete'),
]