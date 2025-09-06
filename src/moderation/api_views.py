from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.models import Bucket
from .serializers import BucketSerializer


class APIBucketListView(ListAPIView):
    queryset = Bucket.objects.all()
    serializer_class = BucketSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


#
# class BucketListView(PermissionRequiredMixin, ListView):
#     model = Bucket
#     paginate_by = 10
#     permission_required = 'content.view_bucket'
#     template_name = 'moderation/bucket_list.html'
#
#     def get_queryset(self):
#         return self.request.user.bucket_set.all()