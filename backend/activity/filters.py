import django_filters
from .models import Activity
from discipline.models import Discipline
from django import forms


class ActivityFilterSet(django_filters.FilterSet):
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
    unit = django_filters.ChoiceFilter(
        choices=Activity._meta.get_field('unit').choices,
        empty_label='Todas',
        label='Unidade',
        widget=forms.Select(
            attrs={
                'class': 'form-select',
                'id': 'unidade'
            }
        )
    )
    period = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Período',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'periodo',
                'Placeholder': 'Buscar por período'
            }
        )
    )

    class Meta:
        model = Activity
        fields = []
