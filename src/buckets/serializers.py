from rest_framework import serializers
from buckets.models import Bucket


class BucketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bucket
        fields = ['id', 'title', 'description', 'slug']


