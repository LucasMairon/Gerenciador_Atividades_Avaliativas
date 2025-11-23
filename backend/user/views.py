from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth import login
from .forms import UserLoginForm, UserPasswordResetForm, UserSetPasswordForm


class UserLoginView(LoginView):
    authentication_form = UserLoginForm
    template_name = 'user/login.html'

    def form_valid(self, form):
        login(self.request, form.get_user())

        if self.request.htmx:
            response = HttpResponse()
            success_url = self.get_success_url()
            response['HX-Redirect'] = success_url
            return response
        
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    next_page = 'user:login'


class UserPasswordResetView(PasswordResetView):
    template_name = 'user/password_reset.html'
    email_template_name = 'user/partials/password_reset_email.html'
    html_email_template_name = 'user/partials/password_reset_email.html'
    success_url = reverse_lazy('user:login')
    form_class = UserPasswordResetForm


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'user/password_reset_confirm.html'
    success_url = reverse_lazy('user:login')
    form_class = UserSetPasswordForm
