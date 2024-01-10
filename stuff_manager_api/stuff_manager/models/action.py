
# from django.contrib.postgres.fields import ArrayField
from django.db import models
from .tag import Tag
from .user import User
from .project import Project

# how can I get an action's history
# -- adding and removing tags counts
# -- adding to history will need to be done using signals

# not sure how to handle this yet, maybe just a date field how I have it is fine
# class DatedActions(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(date__ne=None)

# class ActionCompletion(models.Model):
#     start_time = models.DateTimeField(default=None, null=True)
#     end_time = models.DateTimeField(default=None, null=True)
#     duration = models.PositiveSmallIntegerField()
#     # I want to store notes on the action ie "had to make sure the permissions were correct"
#     # The solution will be to create actual files with the notes
#     # keep duration, etc and auto-add a query || URL to view this note in the app at the top of the file
#     # when you complete stuff, you will be prompted to add duration, start_time, end_time, and arbitrary notes (that you can
#     # mark as useful or not?)

    # -- I want these notes to replace my "completed" folder


class Action(models.Model):
    # save time with no validation ! https://codereview.doctor/features/django/best-practice/charfield-vs-textfield
    description = models.TextField()
    title = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True)

    # date = models.ForeignKey(, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True)
    energy = models.PositiveSmallIntegerField(default=None, null=True)

    # meta_data = models.
    # want to store reason why cannot be done or why 
    # meta_data = models.JSONField()

    # ===================================== foreign keys =====================================
    # each action belongs to a user
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)

    # completion = models.ForeignKey(ActionCompletion, on_delete=models.CASCADE, null=True)

    def __repr__(self):
        return f'Action(title="{self.title}", user={self.user_id}, project={self.project_id}, energy={self.energy})'

    def __str__(self):
        return self.__repr__()




class DelegatedActions(models.Manager):
    # HOW DO I MARK who I delegated too and why
    def get_queryset(self):
        return super().get_queryset().filter(tag__value="delegated")

class SomedayMaybeActions(models.Manager):
    def get_queryset(self):
        # return super().get_queryset().filter(tag__value="somedayMaybe")
        return super().get_queryset().filter(tag__value="someday_maybe")

class CannotBeDoneYetActions(models.Manager):
    # HOW DO I MARK THE REASON ON WHY WE ARE WAITING ON A TASK
    def get_queryset(self):
        return super().get_queryset().filter(tag__value="cannot_be_done_yet")


class Actions_Tags(models.Model):
    # dont delete action if tag deleted!
    action = models.ForeignKey(Action, on_delete=models.PROTECT)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    objects = models.Manager()
    # gtd categories
    delegated = DelegatedActions()
    cannot_be_done_yet = CannotBeDoneYetActions()
    someday_maybe = SomedayMaybeActions()

    def __repr__(self):
        return f'Actions_Tags(action={self.action_id}, tag={self.tag_id})'

    def __str__(self):
        return self.__repr__()


class Actions_RequiredContexts(models.Model):
    action = models.ForeignKey(Action, on_delete=models.PROTECT)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __repr__(self):
        return f'Actions_RequiredContexts(action={self.action_id}, tag={self.tag_id})'

    def __str__(self):
        return self.__repr__()
