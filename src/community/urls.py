from django.urls import path
from community.views import CommunityDetailView, CommunityCreateView


urlpatterns = [
    path('community/', CommunityDetailView.as_view(), name='community-detail'),
    path('community/new', CommunityCreateView.as_view(), name='community-create'),
]