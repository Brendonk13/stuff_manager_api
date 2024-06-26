from django.db import models
from .user import User


class Unprocessed(models.Model):
    title = models.CharField(max_length=128, default="")
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['created']),
        ]

    def __repr__(self):
        return f'Unprocessed(id={self.id}, title="{self.title}", user={self.user_id})'

    def __str__(self):
        return self.__repr__()
