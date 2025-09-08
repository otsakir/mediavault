from rest_framework import serializers
from core.models import Bucket


class BucketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bucket
        fields = ['title', 'description', 'slug']


