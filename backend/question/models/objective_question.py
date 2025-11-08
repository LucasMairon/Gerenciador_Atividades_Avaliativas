from django.db import models
from django.utils.translation import gettext_lazy as _
from .question import Question


class ObjectiveQuestion(Question):
    objective = models.CharField(
        verbose_name=_('Objective'),
        max_length=100,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Questão Objetiva'
        verbose_name_plural = 'Questões Objetivas'
