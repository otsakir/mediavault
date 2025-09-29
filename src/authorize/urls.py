from django.urls import path
from .views import MainLoginView, logout_view
from rest_framework.authtoken.views import obtain_auth_token
# JWT
from .views import MvTokenObtainPairView, MvTokenRefreshView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('authorize/login', MainLoginView.as_view(), name='login'),
    path('authorize/logout', logout_view, name='logout'),
    path('api/login', obtain_auth_token),

    # JWT auth endpoints
    path("api/token/", MvTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", MvTokenRefreshView.as_view(), name="token_refresh"),
]
