from django.urls import path, include
from .views import BucketListView, BucketCreateView, BucketDeleteView, BucketUpdateView, BucketUserListView, \
    BucketTaskListView, SettingsRedirectView
from community.views import CommunityDetailView, CommunityCreateView
from .api_views import APIBucketListView


urlpatterns = [
    path('buckets/', BucketListView.as_view(), name='bucket-list'),
    path('buckets/create', BucketCreateView.as_view(), name='bucket-create'),

    # path('buckets/<int:pk>/', BucketDetailView.as_view(), name='bucket-detail'),
    path('buckets/<int:bucket_id>/delete/', BucketDeleteView.as_view(), name='bucket-delete'),
    path('buckets/<int:bucket_id>/update/', BucketUpdateView.as_view(), name='bucket-update'),

    path('buckets/<int:bucket_id>/settings/', SettingsRedirectView.as_view(), name='bucket-settings'),
    path('buckets/<int:bucket_id>/users/', BucketUserListView.as_view(), name='bucket-user-list'),
    path('buckets/<int:bucket_id>/tasks/', BucketTaskListView.as_view(), name='bucket-task-list'),

    path('community/', CommunityDetailView.as_view(), name='community-detail'),
    path('community/new', CommunityCreateView.as_view(), name='community-create'),


    path('api/buckets', APIBucketListView.as_view(), name='api-bucket-list')

]
