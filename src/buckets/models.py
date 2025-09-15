from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.db import models
from core.security import PermissionSchemeBase
from enum import Enum


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
    modify_permissions = 9
    manage_users = 10
    visit_settings = 11


class BucketPermissionScheme(PermissionSchemeBase):
    """
        Permissions that define the kind of access to a single Bucket object
    """
    Permissions = Permissions




class Bucket(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    slug = AutoSlugField(populate_from='title', unique=True, always_update=False)
    users = models.ManyToManyField(User, through='BucketPermissions')


class BucketPermissions(models.Model):
    bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.CharField(max_length=30, default='.'*30)  # TODO 'default', 'max_length' shouldn't be hardcoded, hmmm...

    @property
    def permission_strings(self):

        perm_scheme = BucketPermissionScheme(self.permission)
        return perm_scheme.allowed_permissions()

    def __str__(self):
        return f'BucketPermission for user {self.user.id} and bucket {self.bucket.id}'



