from django.urls import path
from .views import (BucketListView, BucketDetailView, BucketCreateView, BucketDeleteView, BucketUpdateView, content_root,
                    get_content_item, ContentItemDeleteView, ContentItemPlayerView, ContentItemUpdateView)

urlpatterns = [
    path('buckets/', BucketListView.as_view(), name='bucket-list'),
    path('buckets/<int:pk>/', BucketDetailView.as_view(), name='bucket-detail'),
    path('buckets/create', BucketCreateView.as_view(), name='bucket-create'),
    path('buckets/delete/<int:pk>/', BucketDeleteView.as_view(), name='bucket-delete'),
    path('buckets/update/<int:pk>/', BucketUpdateView.as_view(), name='bucket-update'),

    path('content/<slug:slug>/', content_root, name='content-root'),
    path('content/<slug:slug>/<int:item_id>', get_content_item, name='get-content-item'),
    path('content/<slug:slug>/<int:item_id>/delete', ContentItemDeleteView.as_view(), name='content-item-delete'),
    path('content/<slug:slug>/<int:item_id>/player', ContentItemPlayerView.as_view(), name='content-item-play'),

    path('content/<slug:slug>/<int:item_id>/update', ContentItemUpdateView.as_view(), name='content-item-update'),

]
