from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Community(models.Model):
    name = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from='name', unique=True, always_update=False)


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
