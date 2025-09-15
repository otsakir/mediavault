from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from buckets.models import Bucket, BucketPermissions, Permissions, BucketPermissionScheme
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from content.models import FetchTaskResult
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.db.models import Prefetch


class AuthorizeBucketAccessMixin(UserPassesTestMixin):
    """
        Authorizes access to a bucket for the logged user.

        URL:
            bucket_slug|bucket_id path parameters should be present

        Object state:
            * parent_bucket
            * permission_scheme

        Template context
            * parent_bucket
            * bucket_permissions

    """

    bucket_permission_set = []
    """List of all required permissions for authorization to be granted"""

    parent_bucket = None
    permission_scheme = None

    def test_func(self):
        # self.request.url
        bucket_id = self.kwargs.get('bucket_id', None)
        if not bucket_id:
            raise PermissionDenied("no bucket given")

        try:
            bucket_permissions = BucketPermissions.objects.select_related('bucket').get(bucket=bucket_id, user=self.request.user)

        except BucketPermissions.DoesNotExist as e:
            raise PermissionDenied("no such bucket")
        print("AuthorizeBucketAccessMixin: bucket_permission:", bucket_permissions)

        permission_scheme = BucketPermissionScheme(bucket_permissions.permission)
        if not permission_scheme.allows_all(self.bucket_permission_set):
            raise PermissionDenied("custom permission violation")

        self.parent_bucket = bucket_permissions.bucket
        self.permission_scheme = permission_scheme

        return True
        # bucket = self.get_object()  # TODO catch error thrown when no such object exists to return a generic access related message, not a 404

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['parent_bucket'] = self.parent_bucket
        context['bucket_permissions'] = self.permission_scheme.permissions_as_strings
        return context


class BucketListView(PermissionRequiredMixin, ListView):
    model = Bucket
    paginate_by = 10
    permission_required = 'buckets.view_bucket'
    template_name = 'buckets/bucket_list.html'

    def get_queryset(self):
        logged_user = self.request.user
        return Bucket.objects.prefetch_related(Prefetch('bucketpermissions_set', BucketPermissions.objects.filter(user=logged_user), to_attr='user_permissions')).filter(users=logged_user)


class BucketCreateView(PermissionRequiredMixin, CreateView):
    model = Bucket
    fields = ['title', 'description']
    template_name = 'buckets/bucket_form.html'
    success_url = reverse_lazy('bucket-list')
    permission_required = 'buckets.add_bucket'

    # inject creator user in new bucket object
    def form_valid(self, form):
        instance = form.save()
        # create a BucketPermissions object with default permissions for creators
        instance.users.add(self.request.user, through_defaults={'permission': BucketPermissionScheme.to_permissions_string([
            Permissions.edit_details,
            Permissions.remove,
            Permissions.modify_permissions
        ])})
        return super().form_valid(form)


# class BucketDetailView(DetailView):
#     model = Bucket
#     template_name = 'buckets/bucket_detail.html'


class BucketDeleteView(AuthorizeBucketAccessMixin, DeleteView):
    model = Bucket
    success_url = reverse_lazy('bucket-list')
    bucket_permission_set = [Permissions.remove]
    template_name = 'buckets/bucket_confirm_delete.html'

    pk_url_kwarg = 'bucket_id'


class BucketUpdateView(AuthorizeBucketAccessMixin, UpdateView):
    model = Bucket
    fields = ['title', 'description']
    bucket_permission_set = [Permissions.edit_details]
    template_name = 'buckets/bucket_form.html'
    success_url = reverse_lazy('bucket-list')

    pk_url_kwarg = 'bucket_id'


class BucketSubListView(ListView):
    menuitem = None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['menuitem'] = self.menuitem
        return context


class BucketTaskListView(AuthorizeBucketAccessMixin, BucketSubListView):
    model = FetchTaskResult
    paginate_by = 10
    template_name = 'buckets/bucket_task_list.html'
    bucket_permission_set = [Permissions.view_tasks]

    menuitem = 'tasks'

    def get_queryset(self):
        return FetchTaskResult.objects.filter(bucket=self.parent_bucket)

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     return context

    def get(self, request, *args, **kwargs):
        if request.GET.get('refresh', None):
            return HttpResponseRedirect(reverse('bucket-task-list', kwargs=kwargs))  # redirect to this

        return super().get(self, request, *args, **kwargs)


class BucketUserListView(AuthorizeBucketAccessMixin, BucketSubListView):
    template_name = 'buckets/bucket_user_list.html'
    model = User
    menuitem = 'users'
    bucket_permission_set = [Permissions.manage_users]

    def get_queryset(self):
        return User.objects.filter(bucket=self.parent_bucket)

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     return context
