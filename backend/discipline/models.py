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
    topic = models.CharField(
        verbose_name=_('Topic'),
        max_length=255
    )
    subject = models.CharField(
        verbose_name=_('Subject'),
        max_length=255
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Disciplina')
        verbose_name_plural = _('Disciplinas')
