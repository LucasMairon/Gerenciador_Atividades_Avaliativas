from django.db import models
from django.utils.translation import gettext_lazy as _
from question.models import ObjectiveQuestion
import uuid

ORDER_CHOICES = [
    (1, 'A'),
    (2, 'B'),
    (3, 'C'),
    (4, 'D'),
    (5, 'E')
]


class Alternative(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
        editable=False
    )
    description = models.CharField(
        verbose_name=_('Description'),
        max_length=255
    )
    is_correct = models.BooleanField(
        verbose_name=_('Is Correct'),
        default=False
    )
    question = models.ForeignKey(
        ObjectiveQuestion,
        on_delete=models.CASCADE,
        related_name='alternatives'
    )
    order = models.PositiveIntegerField(
        verbose_name=_('Order'),
        choices=ORDER_CHOICES
    )

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Alternativa'
        verbose_name_plural = 'Alternativas'
