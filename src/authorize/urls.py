from django.urls import path

from .views import MainLoginView

urlpatterns = [
    path('authorize/login', MainLoginView.as_view(), name='login'),
]
