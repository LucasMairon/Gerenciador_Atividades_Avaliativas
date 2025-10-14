from django import forms
from .models import ObjectiveQuestion


class ObjectiveQuestionForm(forms.ModelForm):
    class Meta:
        model = ObjectiveQuestion
        fields = [
            'statement',
            'difficulty_level',
            'visibility',
            'discipline',
            'subject',
            'objective',
        ]
