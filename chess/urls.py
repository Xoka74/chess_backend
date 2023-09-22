from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from chess import settings

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),

    path('bot/', include('bot.urls')),
    path('matchmaking/', include('matchmaking.urls')),
    path('client/', include('client.urls')),
    path('api/', include('api.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
