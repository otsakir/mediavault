from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


class MainLoginView(LoginView):
    template_name = 'authorize/login.html'
    next_page = reverse_lazy('home')



