from django.db import models
from .user import User


class Unprocessed(models.Model):
    title = models.CharField(max_length=128, default="")
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __repr__(self):
        return f'Unprocessed(title="{self.title}", user={self.user_id})'

    def __str__(self):
        return self.__repr__()
