from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.db import models
from core.security import PermissionSchemeBase
from enum import Enum


class BucketPermissionScheme(PermissionSchemeBase):
    """
        Permissions that define the kind of access to a single Bucket object
    """

    class Permissions(Enum):

        view = 0
        edit_details = 1
        remove = 2
        add_content = 3
        remove_content = 4
        play_content = 5
        download_content = 6
        view_tasks = 7
        update_tasks = 8


class Bucket(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    slug = AutoSlugField(populate_from='title', unique=True, always_update=False)
    users = models.ManyToManyField(User, through='BucketPermissions')


class BucketPermissions(models.Model):
    bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.CharField(max_length=30, default='.'*30)  # TODO 'default', 'max_length' shouldn't be hardcoded, hmmm...


