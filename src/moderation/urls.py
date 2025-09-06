from django.urls import path, include
from .views import BucketListView, BucketCreateView, BucketDeleteView, BucketUpdateView, BucketUserListView, CommunityDetailView, CommunityCreateView, BucketTaskListView


urlpatterns = [
    path('buckets/', BucketListView.as_view(), name='bucket-list'),
    path('buckets/create', BucketCreateView.as_view(), name='bucket-create'),
    # path('buckets/<int:pk>/', BucketDetailView.as_view(), name='bucket-detail'),
    path('buckets/delete/<int:pk>/', BucketDeleteView.as_view(), name='bucket-delete'),
    path('buckets/update/<int:pk>/', BucketUpdateView.as_view(), name='bucket-update'),
    path('buckets/<slug:slug>/users/', BucketUserListView.as_view(), name='bucket-user-list'),
    path('buckets/<slug:slug>/tasks/', BucketTaskListView.as_view(), name='bucket-task-list'),

    path('community/', CommunityDetailView.as_view(), name='community-detail'),
    path('community/new', CommunityCreateView.as_view(), name='community-create')

]
