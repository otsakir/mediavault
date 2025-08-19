from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import ForeignKey
from autoslug import AutoSlugField


class Bucket(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    slug = AutoSlugField(populate_from='title', unique=True, always_update=False)


class ContentItem(models.Model):

    class Type(models.TextChoices):
        binary = 'Binary'

    type = models.CharField(choices=Type.choices, max_length=20)
    contentType = ForeignKey(ContentType, on_delete=models.PROTECT)

    bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE, related_name='content_items')


