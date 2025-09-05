from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from core.models import Bucket
from core.views import BucketMembershipMixin
from django.urls import reverse_lazy
from django.contrib.auth.models import User


class BucketListView(PermissionRequiredMixin, ListView):
    model = Bucket
    paginate_by = 10
    permission_required = 'content.view_bucket'
    template_name = 'moderation/bucket_list.html'

    def get_queryset(self):
        return self.request.user.bucket_set.all()


class BucketCreateView(PermissionRequiredMixin, CreateView):
    model = Bucket
    fields = ['title', 'description']
    template_name = 'moderation/bucket_form.html'
    success_url = reverse_lazy('bucket-list')
    permission_required = 'content.add_bucket'

    # inject creator user in new bucket object
    def form_valid(self, form):
        instance = form.save()
        instance.users.add(self.request.user)
        return super().form_valid(form)


# class BucketDetailView(DetailView):
#     model = Bucket
#     template_name = 'moderation/bucket_detail.html'


class BucketDeleteView(PermissionRequiredMixin, DeleteView):
    model = Bucket
    success_url = reverse_lazy('bucket-list')
    permission_required = 'content.delete_bucket'
    template_name = 'moderation/bucket_confirm_delete.html'


class BucketUpdateView(PermissionRequiredMixin, UpdateView):
    model = Bucket
    fields = ['title', 'description']
    permission_required = 'content.change_bucket'
    template_name = 'moderation/bucket_form.html'

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

class BucketUserListView(BucketMembershipMixin, ListView):
    template_name = 'moderation/bucket_test_template.html'
    model = User
    # menuitem = 'users'

    def get_queryset(self):
        print("authorized bucket:", self.bucket)
        users = User.objects.filter(bucket=self.bucket.id)
        print("user found:", len(users))
        return users

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

    #     context['bucket'] = self.authorized_bucket
    #     bucket = self.authorized_bucket
    #     print('bucket:', bucket, bucket.users.all())
    #     return context