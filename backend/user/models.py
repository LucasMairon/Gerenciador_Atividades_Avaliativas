from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from . import validators
from .managers import CustomUserManagers
import uuid


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=100,
        validators=[validators.name_validator]
    )
    personal_email = models.CharField(
        verbose_name=_('Personal Email'),
        max_length=255,
        blank=True,
        null=True,
        validators=[validators.personal_email_validator],
        unique=True
    )
    institutional_email = models.CharField(
        verbose_name=_('Institutional Email'),
        max_length=255,
        unique=True,
        validators=[validators.institutional_email_validator]
    )
    password = models.CharField(
        verbose_name=_('Password'),
        max_length=255,
        validators=[validators.password_validator]
    )
    campus = models.CharField(
        verbose_name=_('Campus'),
        max_length=150
    )
    department = models.CharField(
        verbose_name=_('Department'),
        max_length=255
    )
    is_superuser = models.BooleanField(
        default=False
    )
    is_active = models.BooleanField(
        default=True,
    )
    is_staff = models.BooleanField(
        default=False
    )

    USERNAME_FIELD = 'institutional_email'
    REQUIRED_FIELDS = ['name', 'campus', 'department']
    EMAIL_FIELD = 'institutional_email'
    objects = CustomUserManagers()

    def __str__(self):
        return self.name
