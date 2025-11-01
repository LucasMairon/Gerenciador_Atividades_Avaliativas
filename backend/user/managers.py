from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _


class CustomUserManagers(BaseUserManager):
    def create_user(self, instituional_email, password, **extra_fields):
        if not instituional_email:
            raise ValueError(_("Enter an email"))

        instituional_email = self.normalize_email(instituional_email)
        password = make_password(password)

        if extra_fields.get('personal_email'):
            extra_fields['personal_email'] = self.normalize_email(
                extra_fields['personal_email'])

        user = self.model(
            institutional_email=instituional_email,
            password=password,
            **extra_fields
        )

        user.save(using=self._db)

        return user

    def create_superuser(self, institutional_email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        user = self.create_user(
            institutional_email, password, **extra_fields)

        return user
