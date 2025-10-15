from django import forms
from .models import ObjectiveQuestion, Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'statement',
            'difficulty_level',
            'visibility',
            'discipline',
            'subject',
        ]


class ObjectiveQuestionForm(QuestionForm):
    class Meta:
        model = ObjectiveQuestion
        fields = [
            'objective',
        ]
