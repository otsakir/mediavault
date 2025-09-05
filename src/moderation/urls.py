from django.urls import path, include
from .views import BucketListView, BucketCreateView, BucketDeleteView, BucketUpdateView, BucketUserListView


urlpatterns = [
    path('buckets/', BucketListView.as_view(), name='bucket-list'),
    path('buckets/create', BucketCreateView.as_view(), name='bucket-create'),
    # path('buckets/<int:pk>/', BucketDetailView.as_view(), name='bucket-detail'),
    path('buckets/delete/<int:pk>/', BucketDeleteView.as_view(), name='bucket-delete'),
    path('buckets/update/<int:pk>/', BucketUpdateView.as_view(), name='bucket-update'),

    path('bucket/<int:pk>/users/', BucketUserListView.as_view(), name='bucket-user-list'),


]
