from django.contrib import admin
from .models import ContentItem
from buckets.models import Bucket

# Register your models here.
admin.site.register(Bucket)
admin.site.register(ContentItem)
