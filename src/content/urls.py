from django.urls import path
from .views import (content_root,
                    get_content_item, ContentItemDeleteView, ContentItemPlayerView, ContentItemUpdateView,
                    BucketTaskDeleteAllView)
urlpatterns = [

    path('content/<slug:slug>/', content_root, name='content-root'),
    path('content/<slug:slug>/<int:item_id>', get_content_item, name='get-content-item'),
    path('content/<slug:slug>/<int:item_id>/delete', ContentItemDeleteView.as_view(), name='content-item-delete'),
    path('content/<slug:slug>/<int:item_id>/player', ContentItemPlayerView.as_view(), name='content-item-play'),

    path('content/<slug:slug>/<int:item_id>/update', ContentItemUpdateView.as_view(), name='content-item-update'),

    path('content/<slug:slug>/tasks/delete', BucketTaskDeleteAllView.as_view(), name='bucket-task-list-delete'),

]

