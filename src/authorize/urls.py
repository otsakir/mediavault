from django.urls import path

from .views import MainLoginView, logout_view
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('authorize/login', MainLoginView.as_view(), name='login'),
    path('authorize/logout', logout_view, name='logout'),
    path('api/login', obtain_auth_token),
]
