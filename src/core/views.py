from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Bucket
from django.shortcuts import get_object_or_404
from django.http import Http404


class BucketMembershipMixin(UserPassesTestMixin):
    authorized_bucket = None  # this is set if the user is granted access to this bucket
    bucket_permission_str = 'content.view_contentitem'  # default
    bucket = None

    def test_func(self):
        print("BucketMembershipMixin: in test_func()")
        try:
            self.bucket = Bucket.objects.get(slug=self.kwargs.get('slug'), users__id=self.request.user.id)
        except Bucket.DoesNotExist as e:
            raise Http404('Bucket not accessible')

        return True
