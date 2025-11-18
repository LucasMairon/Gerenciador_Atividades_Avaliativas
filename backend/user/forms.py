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
                'class': 'form-control',
                'id': 'email',
                'placeholder': 'institucional@ufersa.edu.br',
                'required': True
            }
        )
    )

    password = forms.CharField(
        label='Senha',
        validators=[password_validator],
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'password',
                'placeholder': 'Digite a sua senha',
                'required': True
            }
        )
    )
