import django_filters
from .models import Question
from django import forms
from discipline.models import Discipline
from django.contrib.auth.models import User

VISIBILITY_FILTER_CHOICES = (
    (False, 'Privada'),
    (True, 'Compartilhada')
)


class QuestionFilterSet(django_filters.FilterSet):

    type = django_filters.ChoiceFilter(
        choices=Question._meta.get_field('type').choices,
        label='Tipo da questão',
        widget=forms.Select(
            attrs={
                'class': 'form-select',
                'id': 'tipo-questao'
            }
        ),
        empty_label='Todas'
    )

    discipline = django_filters.ModelChoiceFilter(
        queryset=Discipline.objects.all(),
        label='Disciplina',
        empty_label='Todas',
        widget=forms.Select(
            attrs={
                'class': 'form-select',
                'id': 'disciplina'
            }
        )
    )

    difficulty_level = django_filters.ChoiceFilter(
        choices=Question._meta.get_field('difficulty_level').choices,
        empty_label='Todas',
        label='Dificuldade',
        widget=forms.Select(
            attrs={
                'class': 'form-select',
                'id': 'dificuldade'
            }
        )
    )

    visibility = django_filters.ChoiceFilter(
        choices=VISIBILITY_FILTER_CHOICES,
        method='filter_by_visibility',
        label='Visibilidade',
        empty_label='Todas',
        widget=forms.RadioSelect(
            attrs={
                'class': 'form-check-input'
            }
        )
    )

    subject = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Assunto',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'assunto',
                'Placeholder': 'Buscar por assunto'
            }
        )
    )

    topic = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Tópico',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'topico',
                'Placeholder': 'Buscar por tópico'
            }
        )
    )

    statement = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Buscar questão',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'buscar-questao',
                'Placeholder': 'Buscar pelo enunciado da questão'
            }
        )
    )

    owner = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label='Buscar por professor',
        empty_label='Todos',
        widget=forms.Select(
            attrs={
                'class': 'form-select',
                'id': 'disciplina'
            }
        )
    )

    class Meta:
        model = Question
        fields = []

    def filter_by_visibility(self, queryset, name, value):
        if value:
            return queryset.filter(visibility=value)
        else:
            return queryset.filter(visibility=value)
