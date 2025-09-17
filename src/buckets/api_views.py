from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Bucket
from .serializers import BucketSerializer

import time


class APIBucketListView(ListAPIView):
    queryset = Bucket.objects.all()
    serializer_class = BucketSerializer
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        time.sleep(1)
        return super().get_queryset()


class APIBucketCreateView(CreateAPIView):
    serializer_class = BucketSerializer
    authentication_classes = TokenAuthentication
    permission_classes = []

#
# class BucketListView(PermissionRequiredMixin, ListView):
#     model = Bucket
#     paginate_by = 10
#     permission_required = 'content.view_bucket'
#     template_name = 'buckets/bucket_list.html'
#
#     def get_queryset(self):
#         return self.request.user.bucket_set.all()