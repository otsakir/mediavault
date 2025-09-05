from django.db import models
from django.contrib.auth.models import Group

from autoslug import AutoSlugField
from django.contrib.auth.models import User


class Bucket(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    slug = AutoSlugField(populate_from='title', unique=True, always_update=False)
    users = models.ManyToManyField(User)


# class Community(models.Model):
#     name = models.CharField(max_length=50)
#     group = models.OneToOneField(Group, on_delete=models.RESTRICT)

