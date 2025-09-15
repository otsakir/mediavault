from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, CreateView
from django.views.generic.edit import FormMixin

from community.models import Community
from buckets.services import CommunityService
from core.breadcrumbs import Breadcrumb


# Create your views here.
class CommunityDetailView(LoginRequiredMixin, DetailView):
    template_name = 'community/community_detail_template.html'

    def get_object(self, queryset=None):

        member = self.request.user.get_member()
        if member:
            return member.community

        return None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['breadcrumbs'] = [
            Breadcrumb('Community', None),
        ]
        return context


class CommunityCreateView(LoginRequiredMixin, CreateView):
    template_name = 'community/community_form.html'
    model = Community
    fields = ['name']
    success_url = reverse_lazy('community-detail')

    def form_valid(self, form):
        self.object = CommunityService.create_community(self.request.user, form.cleaned_data['name'])
        return FormMixin.form_valid(self, form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['breadcrumbs'] = [
            Breadcrumb('Community', reverse('community-detail', kwargs=kwargs)),
            Breadcrumb('New', None),
        ]
        return context