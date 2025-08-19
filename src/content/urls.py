from django.urls import path
from .views import BucketListView, BucketDetailView, BucketCreateView, BucketDeleteView, BucketUpdateView

urlpatterns = [
    path('buckets/', BucketListView.as_view(), name='bucket-list'),
    path('buckets/<int:pk>/', BucketDetailView.as_view(), name='bucket-detail'),
    path('buckets/create', BucketCreateView.as_view(), name='bucket-create'),
    path('buckets/delete/<int:pk>/', BucketDeleteView.as_view(), name='bucket-delete'),
    path('buckets/update/<int:pk>/', BucketUpdateView.as_view(), name='bucket-update'),
]
