
from django.contrib.postgres.fields import ArrayField
from django.db import models
from .tag import Tag
from functools import partial

class DelegatedActions(models.Manager):
    # can notes ever go in the someday/maybe category?
    # -- yes
    def get_queryset(self):
        return super().get_queryset().filter(tag__value="somedayMaybe")
        # return Actions_Tags.objects.filter()

class CannotBeDoneYetActions(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(tag__value="CannotBeDoneYet")

# class DatedActions(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(date__ne=None)







class Action(models.Model):
    class Meta:
        ordering = ['created']
    # FEATURE: what if this action could reference a non-actionable item of any sort

    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128)

    # save time with no validation !
    # https://codereview.doctor/features/django/best-practice/charfield-vs-textfield
    description = models.TextField()

    date = models.DateTimeField(null=True)
    # date = models.ForeignKey(, on_delete=models.CASCADE)

    # dates = ArrayField(models.DateTimeField(), default=list, blank=True)
    tags = ArrayField(models.CharField(max_length=64, null=True), default=list, blank=True)
    context = ArrayField(models.CharField(max_length=64, null=True), default=list, blank=True)

    # tags = models.CharField(max_length=64, null=True)


class Actions_Tags(models.Model):
    # dont delete action if tag deleted!
    action = models.ForeignKey(Action, on_delete=models.PROTECT)

    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    delegated = DelegatedActions()

