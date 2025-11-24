from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class Discipline(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        unique=True,
        default=uuid.uuid4
    )
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=255
    )
    code = models.CharField(
        verbose_name=_('Code'),
        max_length=10
    )

    def __str__(self):
        return f'{self.name} - {self.code}'

    class Meta:
        verbose_name = _('Disciplina')
        verbose_name_plural = _('Disciplinas')
