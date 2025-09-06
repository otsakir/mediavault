from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.views.generic.edit import FormMixin
from core.models import Bucket, Community
from core.views import BucketMembershipMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from moderation.services import CommunityService
from content.models import FetchTaskResult
from django.http import HttpResponseRedirect


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


class CommunityDetailView(LoginRequiredMixin, DetailView):
    template_name = 'moderation/community_detail_template.html'

    def get_object(self, queryset=None):

        member = self.request.user.get_member()
        if member:
            return member.community

        return None


class CommunityCreateView(LoginRequiredMixin, CreateView):
    template_name = 'moderation/community_form.html'
    model = Community
    fields = ['name']
    success_url = reverse_lazy('community-detail')

    def form_valid(self, form):
        self.object = CommunityService.create_community(self.request.user, form.cleaned_data['name'])
        return FormMixin.form_valid(self, form)


class BucketSubListView(ListView):
    menuitem = None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['menuitem'] = self.menuitem
        return context


class BucketTaskListView(BucketMembershipMixin, BucketSubListView):
    model = FetchTaskResult
    paginate_by = 10
    template_name = 'moderation/bucket_task_list.html'
    menuitem = 'tasks'

    def get_queryset(self):
        return FetchTaskResult.objects.filter(bucket=self.authorized_bucket)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['bucket'] = self.bucket
        return context

    def get(self, request, *args, **kwargs):
        if request.GET.get('refresh', None):
            return HttpResponseRedirect(reverse('bucket-task-list', kwargs=kwargs))  # redirect to this

        return super().get(self, request, *args, **kwargs)


class BucketUserListView(BucketMembershipMixin, BucketSubListView):
    template_name = 'moderation/bucket_user_list.html'
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


