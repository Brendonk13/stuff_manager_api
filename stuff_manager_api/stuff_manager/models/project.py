from django.db import models
from .user import User

class Project(models.Model):
    name = models.CharField(max_length=128)
    notes = models.TextField()
    # not sure what else should be here

class Projects_User(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    project = models.ForeignKey(Project, on_delete=models.PROTECT)

