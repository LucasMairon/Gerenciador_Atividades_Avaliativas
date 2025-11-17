from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from .validators import institutional_email_validator, password_validator


class UserLoginForm(AuthenticationForm):

    username = forms.EmailField(
        label='Email Institucional',
        validators=[institutional_email_validator],
        widget=forms.EmailInput(
            attrs={
                'class': 'email_class_here',
                'id': 'email_id_here',
                'placeholder': 'email_placeholder_here'
            }
        )
    )

    password = forms.CharField(
        label='Senha',
        validators=[password_validator],
        widget=forms.PasswordInput(
            attrs={
                'class': 'password_class_here',
                'id': 'password_id_here',
                'placeholder': 'password_placeholder_here'
            }
        )
    )
