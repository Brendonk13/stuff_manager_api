from django.db import models

class Tag(models.Model):
    value = models.CharField(max_length=64)

    def __repr__(self):
        return f'Tag(value="{self.value}")'

    def __str__(self):
        return self.__repr__()
