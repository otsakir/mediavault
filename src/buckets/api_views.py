from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Bucket
from .serializers import BucketSerializer

import time


class APIBucketListCreateView(ListCreateAPIView):
    queryset = Bucket.objects.all()
    serializer_class = BucketSerializer
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        time.sleep(1)
        return super().get_queryset()


class APIBucketRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Bucket.objects.all()
    serializer_class = BucketSerializer

    lookup_url_kwarg = 'bucket_id'
    lookup_field = 'id'
