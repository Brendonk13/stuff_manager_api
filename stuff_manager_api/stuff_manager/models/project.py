from django.db import models
from .user import User

class Project(models.Model):
    name = models.CharField(max_length=128)
    notes = models.TextField()
    # not sure what else should be here

    def __repr__(self):
        return f"Project(id={self.id}, name={self.name})"

class Projects_User(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    project = models.ForeignKey(Project, on_delete=models.PROTECT)

    def __repr__(self):
        return f"Projects_User(id={self.id}, user={self.user_id}, project={self.project_id})"

