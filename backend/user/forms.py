from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
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
                'placeholder': 'Exemplo@ufersa.edu.br',
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


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        validators=[institutional_email_validator],
        label='Email Institucional',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Exemplo@ufersa.edu.br',
                'class': 'form-control',
                'id': 'email_reset',
                'required': True
            }
        )
    )


class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='Nova Senha',
        validators=[password_validator],
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'password1',
                'placeholder': 'D@cente10',
                'required': True
            }
        )
    )
    new_password2 = forms.CharField(
        label='Confirme a Senha',
        validators=[password_validator],
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'password2',
                'placeholder': 'D@cente10',
                'required': True
            }
        )
    )
