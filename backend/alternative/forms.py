from django import forms
from .models import Alternative


class AlternativeForm(forms.ModelForm):
    class Meta:
        model = Alternative
        fields = ['description', 'is_correct', 'order']

        widgets = {
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'teste',
                    'rows': 1
                }
            ),
            'is_correct': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input mt-0'
                }
            )
        }
