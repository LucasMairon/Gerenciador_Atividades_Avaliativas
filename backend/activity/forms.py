from django import forms
from .models import Activity


class ActivityForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['discipline'].empty_label = 'Selecione uma disciplina'
        unit_choices = list(
            self.fields['unit'].choices)
        unit_choices.pop(0)

        default_unit_choice = [("", 'Selecione uma unidade')]

        self.fields['unit'].choices = default_unit_choice + \
            unit_choices

    class Meta:
        model = Activity
        fields = [
            'name',
            'unit',
            'discipline',
            'period'
        ]
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'nome',
                    'placeholder': 'Ex: Avaliação/Lista de exercício'
                }
            ),
            'discipline': forms.Select(
                attrs={
                    'class': 'form-select',
                    'id': 'disciplina',
                    'placeholder': 'Selecione uma disciplina'
                }
            ),
            'period': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'periodo',
                    'placeholder': 'Ex:2025.2'
                }
            ),
            'unit': forms.Select(
                attrs={
                    'class': 'form-select',
                    'id': 'unidade'
                }
            )
        }
        labels = {
            'name': 'Nome da atividade',
            'discipline': 'Disciplina',
            'period': 'Período',
            'unit': 'Unidade'
        }
