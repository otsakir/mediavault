import os.path

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

    class HttpContentType(models.TextChoices):
        application_octet_stream = 'application/octet-stream'
        mp4_video = "video/mp4"

    type = models.CharField(choices=Type.choices, max_length=20)
    content_type = models.CharField(choices=HttpContentType.choices, max_length=50, default=HttpContentType.application_octet_stream)
    title = models.CharField(max_length=100, default='untitled')
    file = models.FileField()
    bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE, related_name='content_items')
    streaming = models.BooleanField(default=False)  # stream instead of download

    def delete(self, using=None, keep_parents=False):
        file_path = None
        if self.file and os.path.isfile(self.file.path):
            file_path = self.file.path

        delete_result = super().delete(using, keep_parents)
        deleted_count, _ = delete_result

        # TODO: make sure the path is indeed under MEDIA_ROOT!! (right?)
        # remove the underlying file too
        if file_path and (deleted_count > 0):
            os.remove(file_path)

        return delete_result

