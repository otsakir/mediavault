from django.db import models
from django.contrib.auth.models import Group

from autoslug import AutoSlugField
from django.contrib.auth.models import User


class Bucket(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    slug = AutoSlugField(populate_from='title', unique=True, always_update=False)
    users = models.ManyToManyField(User, through='BucketPermissions')


class BucketPermissions(models.Model):
    bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.IntegerField(default=0)



class Community(models.Model):
    name = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from='name', unique=True, always_update=False)


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)


# attach helper method to User class
def get_member(user):
    try:
        return user.member
    except Member.DoesNotExist as e:
        return None


User.add_to_class('get_member', get_member)


