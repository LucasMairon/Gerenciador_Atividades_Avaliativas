from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import User
from question.models import Question
from discipline.models import Discipline
from . import validators
import uuid

UNIT_CHOICES = [
    (1, 'I'),
    (2, 'II'),
    (3, 'III'),
]


class Activity(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=255
    )
    unit = models.PositiveSmallIntegerField(
        verbose_name=_('Unit'),
        choices=UNIT_CHOICES
    )
    period = models.CharField(
        verbose_name=_('Period'),
        max_length=5,
        validators=[validators.period_validator]
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Owner')
    )
    use_count = models.PositiveIntegerField(
        _('Use count'),
        default=0
    )
    subject = models.CharField(
        verbose_name=_('Subject'),
        max_length=255,
        blank=True,
        null=True,
    )
    topic = models.CharField(
        verbose_name=_('Topic'),
        max_length=255,
        blank=True,
        null=True,
    )
    questions = models.ManyToManyField(
        Question,
        related_name='activities',
        through="QuestionActivity",
        verbose_name=_('Activity questions')
    )
    discipline = models.ForeignKey(
        Discipline,
        verbose_name=_('Discipline'),
        on_delete=models.PROTECT,
        related_name='activities'
    )
    created_at = models.DateTimeField(
        verbose_name=_('Created at'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_('Updated at'),
        auto_now=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Atividade'
        verbose_name_plural = 'Atividades'


class QuestionActivity(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    order = models.PositiveIntegerField(
        verbose_name=_('Order')
    )

    class Meta:
        verbose_name = 'Questão de atividade'
        verbose_name_plural = 'Questões de atividades'
        unique_together = [['activity', 'order'], ['activity', 'question']]
