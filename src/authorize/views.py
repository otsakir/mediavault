from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth import logout

class MainLoginView(LoginView):
    template_name = 'authorize/login.html'
    next_page = reverse_lazy('home')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('login'))


