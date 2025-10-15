from django import forms
from .models import ObjectiveQuestion, Question, SubjectiveQuestion


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


class SubjectiveQuestionForm(QuestionForm):
    class Meta:
        model = SubjectiveQuestion
        fields = [
            'expected_answer',
            'key_answers',
        ]
