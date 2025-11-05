from django import forms
from .models import Activity


class ActivityForm(forms.ModelForm):
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
