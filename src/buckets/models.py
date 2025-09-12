from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Bucket(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    slug = AutoSlugField(populate_from='title', unique=True, always_update=False)
    users = models.ManyToManyField(User, through='BucketPermissions')


class BucketPermissions(models.Model):
    bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.IntegerField(default=0)
