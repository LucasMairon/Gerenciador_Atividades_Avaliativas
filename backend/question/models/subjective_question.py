from django.db import models
from django.utils.translation import gettext_lazy as _
from .question import Question


class SubjectiveQuestion(Question):
    expected_answer = models.CharField(
        verbose_name=_('Expected answer'),
        max_length=500
    )
    key_answers = models.CharField(
        verbose_name=_('Key answers'),
        max_length=100,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Questão Subjetiva'
        verbose_name_plural = 'Questões Subjetivas'
