from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from discipline.models import Discipline
import uuid

DIFFICULTY_CHOICES = [
    ('E', _('Easy')),
    ('M', _('Medium')),
    ('D', _('Difficult'))
]

VISIBILITY_CHOICES = [
    (True, _('Public')),
    (False, _('Private'))
]

TYPE_CHOICES = [
    ('O', 'Objective'),
    ('S', 'Subjective')
]


class Question(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        unique=True,
        default=uuid.uuid4
    )
    owner = models.ForeignKey(
        User,
        verbose_name=_('Owner'),
        on_delete=models.CASCADE,
        related_name='%(class)s_questions'
    )
    difficulty_level = models.CharField(
        verbose_name=_('Difficulty level'),
        choices=DIFFICULTY_CHOICES,
        max_length=1
    )
    visibility = models.BooleanField(
        verbose_name=_('Visibility'),
        choices=VISIBILITY_CHOICES,
        default=False
    )
    statement = models.TextField(
        verbose_name=_('Statement')
    )
    subject = models.TextField(
        verbose_name=_('Subject')
    )
    use_count = models.PositiveIntegerField(
        _('Use count'),
        default=0
    )
    type = models.CharField(
        _('Type'),
        max_length=1,
        choices=TYPE_CHOICES
    )
    is_active = models.BooleanField(
        verbose_name=_('Is active'),
        default=True
    )
    created_at = models.DateTimeField(
        verbose_name=_('Created at'),
        auto_now_add=True
    )
    updated_at = models.DateField(
        verbose_name=_('Updated at'),
        auto_now=True
    )
    discipline = models.ForeignKey(
        Discipline,
        verbose_name=_('Discipline'),
        on_delete=models.PROTECT,
        related_name='%(class)s_questions'
    )

    class Meta:
        verbose_name = 'Questão'
        verbose_name_plural = 'Questões'
