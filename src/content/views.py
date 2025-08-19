from django.shortcuts import render
from content.models import Bucket
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy


class BucketListView(ListView):
    model = Bucket
    paginate_by = 10

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context


class BucketCreateView(CreateView):
    model = Bucket
    fields = ['title', 'description']
    template_name = 'content/bucket_form.html'

    # if you cant to manually set the slug, uncomment:
    # def form_valid(self, form):
    #     # get the underlying model instance and update slug
    #     instance = form.save(commit=False)
    #     instance.slug = slugify(instance.title)
    #     return super().form_valid(form)

    success_url = reverse_lazy('bucket-list')


class BucketDetailView(DetailView):
    model = Bucket

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_


class BucketDeleteView(DeleteView):
    model = Bucket
    success_url = reverse_lazy('bucket-list')


class BucketUpdateView(UpdateView):
    model = Bucket
    fields = ['title', 'description']

    success_url = reverse_lazy('bucket-list')

