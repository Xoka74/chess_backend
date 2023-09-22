import uuid

from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class UserIntent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)

    @database_sync_to_async
    def auser(self):
        return self.user
