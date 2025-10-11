from django.db import models
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from .question import Question

MAX_NUMBER_ALTERNATIVES = 5
MIN_NUMBER_ALTERNATIVES = 4


class ObjectiveQuestion(Question):
    objective = models.CharField(
        verbose_name=_('Objective'),
        max_length=100
    )

    def __str__(self):
        return self.statement

    def clean(self):
        super().clean()

        if self.pk:
            alternatives_count = self.alternatives.count()
            if alternatives_count > MAX_NUMBER_ALTERNATIVES and alternatives_count < MIN_NUMBER_ALTERNATIVES:
                raise ValidationError(
                    f'Número de alternativas inválidas, por favor coloque o número de alternativas entre ${MAX_NUMBER_ALTERNATIVES} e ${MIN_NUMBER_ALTERNATIVES}, atualmente possui ${alternatives_count}'
                )

    class Meta:
        verbose_name = 'Questão Objetiva'
        verbose_name_plural = 'Questões Objetivas'
