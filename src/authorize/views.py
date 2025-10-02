from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth import logout
# JWT
from rest_framework_simplejwt.views import TokenObtainPairView
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

