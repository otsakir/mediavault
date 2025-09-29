from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth import logout
from rest_framework.request import Request
from rest_framework.response import Response
# JWT
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import MvTokenObtainPairSerializer

class MainLoginView(LoginView):
    template_name = 'authorize/login.html'
    next_page = reverse_lazy('home')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('login'))


# JWT
class MvTokenObtainPairView(TokenObtainPairView):
    serializer_class = MvTokenObtainPairSerializer

class MvTokenRefreshView(TokenRefreshView):

    def post(self, request: Request, *args, **kwargs) -> Response:

        return super().post(request, *args, **kwargs)


