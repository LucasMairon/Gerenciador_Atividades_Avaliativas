from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserLoginForm


class UserLoginView(LoginView):
    authentication_form = UserLoginForm
    template_name = 'user/login.html'


class UserLogoutView(LogoutView):
    next_page = 'user:login'
