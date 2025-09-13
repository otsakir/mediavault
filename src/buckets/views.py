from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from buckets.models import Bucket, BucketPermissions
from core.views import BucketMembershipMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from content.models import FetchTaskResult
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied




# class AuthorizeBucketAccessMixin(UserPassesTestMixin):
#     authorized_bucket = None  # this is set if the user is granted access to this bucket
#     bucket_permission_str = 'content.view_contentitem'  # default
#
#     def test_func(self):
#         # print("AuthorizeBucketAccessMixin: in test_func()", self.kwargs.get('slug'))
#         self.authorized_bucket = authorize_bucket_access(self.request, self.kwargs.get('slug'), self.bucket_permission_str)
#         return True

class AuthorizeBucketAccessMixin(UserPassesTestMixin):
    """
        Authorizes access to a bucket for the logged user.

        URL:
           bucket_slug|bucket_id path parameters should be present
    """

    slug_url_kwarg = "bucket_slug"
    pk_url_kwarg = "bucket_id"

    permission_set = []
    """List of all required permissions for authorization to be granted"""

    def test_func(self):
        try:
            bp = BucketPermissions.objects.get(bucket=self.get_object(), user=self.request.user)
        except BucketPermissions.DoesNotExist as e:
            raise PermissionDenied()
        print("AuthorizeBucketAccessMixin: bucket_permission:", bp)

        return True
        # bucket = self.get_object()  # TODO catch error thrown when no such object exists to return a generic access related message, not a 404


class BucketListView(PermissionRequiredMixin, ListView):
    model = Bucket
    paginate_by = 10
    permission_required = 'content.view_bucket'
    template_name = 'buckets/bucket_list.html'

    def get_queryset(self):
        return self.request.user.bucket_set.all()


class BucketCreateView(PermissionRequiredMixin, CreateView):
    model = Bucket
    fields = ['title', 'description']
    template_name = 'buckets/bucket_form.html'
    success_url = reverse_lazy('bucket-list')
    permission_required = 'content.add_bucket'

    # inject creator user in new bucket object
    def form_valid(self, form):
        instance = form.save()
        instance.users.add(self.request.user)
        return super().form_valid(form)


# class BucketDetailView(DetailView):
#     model = Bucket
#     template_name = 'buckets/bucket_detail.html'


class BucketDeleteView(PermissionRequiredMixin, DeleteView):
    model = Bucket
    success_url = reverse_lazy('bucket-list')
    permission_required = 'content.delete_bucket'
    template_name = 'buckets/bucket_confirm_delete.html'


class BucketUpdateView(AuthorizeBucketAccessMixin, UpdateView):
    model = Bucket
    fields = ['title', 'description']
    permission_required = 'content.change_bucket'
    template_name = 'buckets/bucket_form.html'

    success_url = reverse_lazy('bucket-list')


# class BucketUserListView(BucketMembershipMixin, BucketSubListView):
#     template_name = 'content/bucket_user_list.html'
#     model = User
#     menuitem = 'users'
#
#     def get_queryset(self):
#         return User.objects.filter(bucket=self.authorized_bucket)
#
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         context['bucket'] = self.authorized_bucket
#         bucket = self.authorized_bucket
#         print('bucket:', bucket, bucket.users.all())
#         return context


class BucketSubListView(ListView):
    menuitem = None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['menuitem'] = self.menuitem
        return context


class BucketTaskListView(BucketMembershipMixin, BucketSubListView):
    model = FetchTaskResult
    paginate_by = 10
    template_name = 'buckets/bucket_task_list.html'
    menuitem = 'tasks'

    def get_queryset(self):
        return FetchTaskResult.objects.filter(bucket=self.bucket)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['bucket'] = self.bucket
        return context

    def get(self, request, *args, **kwargs):
        if request.GET.get('refresh', None):
            return HttpResponseRedirect(reverse('bucket-task-list', kwargs=kwargs))  # redirect to this

        return super().get(self, request, *args, **kwargs)


class BucketUserListView(BucketMembershipMixin, BucketSubListView):
    template_name = 'buckets/bucket_user_list.html'
    model = User
    menuitem = 'users'

    def get_queryset(self):
        print("authorized bucket:", self.bucket)
        users = User.objects.filter(bucket=self.bucket.id)
        print("user found:", len(users))
        return users

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['bucket'] = self.bucket

        member = self.request.user.get_member()
        if member:
            context['community_members'] = member.community

        return context


