from django.contrib.auth.views import LoginView
from .forms import UserLoginForm


class UserLoginView(LoginView):
    authentication_form = UserLoginForm
    template_name = 'user/login.html'
