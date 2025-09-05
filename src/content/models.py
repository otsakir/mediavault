import os.path

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from core.models import Bucket


class ContentItem(models.Model):

    class Meta:
        permissions = [
            ('download_contentitem', 'Can download content item'),
        ]

    class Type(models.TextChoices):
        binary = 'Binary'

    class HttpContentType(models.TextChoices):
        application_octet_stream = 'application/octet-stream'
        mp4_video = "video/mp4"
        mp4_audio = "audio/mp4"

    type = models.CharField(choices=Type.choices, max_length=20)
    content_type = models.CharField(choices=HttpContentType.choices, max_length=50, default=HttpContentType.application_octet_stream)
    title = models.CharField(max_length=100, default='untitled')
    file = models.FileField() # blank=True, null=True)
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


class FetchTaskResult(models.Model):

    class Meta:
        ordering = ['-started_at']

    class Status(models.TextChoices):
        started = 'Started'
        finished = 'Finished'
        error = 'Finished with error'

    bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=Status.choices, default=Status.started)
    error = models.TextField(blank=True)
    text = models.TextField(default='', blank=True, null=True)
