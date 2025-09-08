from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView
from django.views.generic.edit import FormMixin

from community.models import Community
from moderation.services import CommunityService


# Create your views here.
class CommunityDetailView(LoginRequiredMixin, DetailView):
    template_name = 'community/community_detail_template.html'

    def get_object(self, queryset=None):

        member = self.request.user.get_member()
        if member:
            return member.community

        return None


class CommunityCreateView(LoginRequiredMixin, CreateView):
    template_name = 'community/community_form.html'
    model = Community
    fields = ['name']
    success_url = reverse_lazy('community-detail')

    def form_valid(self, form):
        self.object = CommunityService.create_community(self.request.user, form.cleaned_data['name'])
        return FormMixin.form_valid(self, form)
