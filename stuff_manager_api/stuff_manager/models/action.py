
# from django.contrib.postgres.fields import ArrayField
from django.db import models
from .tag import Tag
from .user import User

# how can I get an action's history
# -- adding and removing tags counts
# -- adding to history will need to be done using signals

class DelegatedActions(models.Manager):
    # HOW DO I MARK who I delegated too and why
    def get_queryset(self):
        return super().get_queryset().filter(tag__value="delegate")

class SomedayMaybeActions(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(tag__value="somedayMaybe")

class CannotBeDoneYetActions(models.Manager):
    # HOW DO I MARK THE REASON ON WHY WE ARE WAITING ON A TASK
    def get_queryset(self):
        return super().get_queryset().filter(tag__value="CannotBeDoneYet")

# not sure how to handle this yet, maybe just a date field how I have it is fine
# class DatedActions(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(date__ne=None)


class Project(models.Model):
    name = models.CharField(max_length=128)
    notes = models.TextField()
    # not sure what else should be here

class Projects_User(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    project = models.ForeignKey(Project, on_delete=models.PROTECT)


class Action(models.Model):

    created = models.DateTimeField(auto_now_add=True)

    # each action belongs to a user
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)

    # save time with no validation !
    # https://codereview.doctor/features/django/best-practice/charfield-vs-textfield
    description = models.TextField()
    title = models.CharField(max_length=128)

    # date = models.ForeignKey(, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True)

    # meta_data = models.
    # want to store reason why cannot be done or why 
    # meta_data = models.JSONField()

    # HOW DO I MARK THE REASON ON WHY WE ARE WAITING ON A TASK


class Actions_Tags(models.Model):
    # dont delete action if tag deleted!
    action = models.ForeignKey(Action, on_delete=models.PROTECT)

    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


    # gtd categories
    delegated = DelegatedActions()
    cannot_be_done = CannotBeDoneYetActions()
    someday_maybe = SomedayMaybeActions()


class Actions_RequiredContexts(models.Model):
    action = models.ForeignKey(Action, on_delete=models.PROTECT)

    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
