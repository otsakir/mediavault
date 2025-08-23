import os, re

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponse, FileResponse, HttpResponseNotModified, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.utils.http import http_date
from django.views.static import was_modified_since

from content.models import Bucket, ContentItem
from django.views.generic import ListView, DetailView, DeleteView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django import forms


class BucketListView(PermissionRequiredMixin, ListView):
    model = Bucket
    paginate_by = 10
    permission_required = 'content.view_bucket'

    def get_queryset(self):
        return self.request.user.bucket_set.all()


class BucketCreateView(PermissionRequiredMixin, CreateView):
    model = Bucket
    fields = ['title', 'description']
    template_name = 'content/bucket_form.html'
    success_url = reverse_lazy('bucket-list')
    permission_required = 'content.add_bucket'

    # inject creator user in new bucket object
    def form_valid(self, form):
        instance = form.save()
        instance.users.add(self.request.user)
        return super().form_valid(form)


class BucketDetailView(DetailView):
    model = Bucket


class BucketDeleteView(PermissionRequiredMixin, DeleteView):
    model = Bucket
    success_url = reverse_lazy('bucket-list')
    permission_required = 'content.delete_bucket'


class BucketUpdateView(PermissionRequiredMixin, UpdateView):
    model = Bucket
    fields = ['title', 'description']
    permission_required = 'content.change_bucket'

    success_url = reverse_lazy('bucket-list')


class ContentUploadForm(forms.Form):

    title = forms.CharField()
    file = forms.FileField()
    content_type = forms.ChoiceField(choices=ContentItem.HttpContentType.choices)
    streaming = forms.BooleanField(required=False, label='Streamable')


def authorize_bucket_access(request, bucket_slug, permission_str):
    print('checking permission:', permission_str)
    has_perm = request.user.has_perm(permission_str)
    print('has_perm:', has_perm)
    if not request.user.has_perm(permission_str):
        print("Permission denied")
        raise PermissionDenied("You can't access this bucket.") # no permission
    bucket = get_object_or_404(Bucket, slug=bucket_slug)
    if not bucket.users.contains(request.user):
        raise PermissionDenied("You can't access this bucket.")

    return bucket


# handles uploading files
@login_required
def content_root(request, slug):
    bucket = authorize_bucket_access(request, slug, 'content.view_contentitem')

    form = ContentUploadForm()
    content_items_list = []
    if request.method == 'POST':
        bucket = authorize_bucket_access(request, slug, 'content.add_contentitem') # TODO make sure to re-use the bucket object that is already loaded
        form = ContentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            content_item = ContentItem(**form.cleaned_data, type=ContentItem.Type.binary, bucket=bucket) # content type is by default binary in the model
            content_item.save()
            redirect_url = reverse_lazy('content-root', kwargs={'slug': slug}) + f'?uploaded=yes'
            return HttpResponseRedirect(redirect_url)
    elif request.method == 'GET':
        content_items = ContentItem.objects.filter(bucket=bucket)
        content_items_list = [{'id': item.id, 'title': item.title, 'streaming': item.streaming} for item in content_items]

    return render(request, 'content/content_root.html', {
        'bucket': {'title': bucket.title, 'slug': bucket.slug},
        'form': form,
        'uploaded': request.GET.get('uploaded', None),
        'content_items': content_items_list})


@login_required
def get_content_item(request, slug, item_id):
    bucket = authorize_bucket_access(request, slug, 'content.download_contentitem')

    streaming = request.GET.get('streaming', None)
    content_item = ContentItem.objects.get(id=item_id, bucket__slug=slug)
    if not content_item:
        return HttpResponse(status=404) # TODO properly handle not found, unauthorized etc.

    if streaming and content_item.streaming:
        return stream_ranged(request, content_item)
    else:
        file = content_item.file.open('rb')
        return FileResponse(file, as_attachment=True, filename=content_item.title)


def stream_ranged(request, content_item):
    file_path = content_item.file.path
    file_size = os.path.getsize(file_path)

    # Handle If-Modified-Since
    if not was_modified_since(request.META.get('HTTP_IF_MODIFIED_SINCE'), os.path.getmtime(file_path)):
        return HttpResponseNotModified()

    # Handle Range requests for seeking
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_match = re.match(r'bytes=(\d+)-(\d+)?', range_header) if range_header else None

    if range_match:
        start_byte = int(range_match.group(1))
        end_byte = int(range_match.group(2)) if range_match.group(2) else file_size - 1

        print("start_byte - end_byte:", start_byte, end_byte)

        if start_byte >= file_size:
            return HttpResponse(status=416)

        MAX_CHUNK_SIZE = 5000000
        if end_byte-start_byte+1 > MAX_CHUNK_SIZE:
            end_byte = start_byte + MAX_CHUNK_SIZE - 1

        length = end_byte - start_byte + 1
        response = HttpResponse(status=206)
        response['Content-Range'] = f'bytes {start_byte}-{end_byte}/{file_size}'
        response['Content-Length'] = str(length)

        with open(file_path, 'rb') as f:
            f.seek(start_byte)
            response.content = f.read(length)
    else:
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Length'] = str(file_size)

    response['Content-Type'] = content_item.content_type
    response['Accept-Ranges'] = 'bytes'
    response['Last-Modified'] = http_date(os.path.getmtime(file_path))

    return response


class AuthorizeBucketAccessMixin(UserPassesTestMixin):
    authorized_bucket = None  # this is set if the user is granted access to this bucket
    bucket_permission_str = 'content.view_contentitem'  # default

    def test_func(self):
        print("AuthorizeBucketAccessMixin: in test_func()", self.kwargs.get('slug'))
        self.authorized_bucket = authorize_bucket_access(self.request, self.kwargs.get('slug'), self.bucket_permission_str)
        return True


class ContentItemSingleObjectMixin(AuthorizeBucketAccessMixin, SingleObjectMixin):
    model = ContentItem
    pk_url_kwarg = 'item_id'

    def get_object(self, queryset=None):
        content_item = ContentItem.objects.get(id=self.kwargs.get('item_id'), bucket=self.authorized_bucket)
        if not content_item:
            return HttpResponse(status=404)

        return content_item


class ContentItemDeleteView(ContentItemSingleObjectMixin, DeleteView):
    template_name = 'content/contentitem_confirm_delete.html'
    bucket_permission_str = 'content.delete_contentitem'

    def get_success_url(self):
        return reverse_lazy('content-root', args=[self.kwargs['slug']])


class ContentItemPlayerView(ContentItemSingleObjectMixin, DetailView):
    template_name = 'content/contentitem_video_player.html'
    bucket_permission_str = 'content.download_contentitem'


class ContentItemUpdateView(ContentItemSingleObjectMixin, UpdateView):
    template_name = 'content/contentitem_update_fields.html'
    fields = ['title', 'content_type', 'streaming']
    bucket_permission_str = 'content.change_contentitem'

    def get_success_url(self):
        return reverse_lazy('content-root', args=[self.kwargs['slug']])
