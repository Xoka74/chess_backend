from django.contrib import admin

from users.models import User, FriendRequest

admin.site.register(User)
admin.site.register(FriendRequest)
