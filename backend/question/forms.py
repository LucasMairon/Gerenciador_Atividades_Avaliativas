from django import forms
from .models import ObjectiveQuestion, Question, SubjectiveQuestion
from alternative.forms import AlternativeForm
from alternative.models import Alternative


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


QuestionAlternativesFormSet = forms.inlineformset_factory(
    parent_model=ObjectiveQuestion,
    model=Alternative,
    form=AlternativeForm,
    extra=0,
    max_num=5,
    min_num=4,
    can_delete=False,
)


class SubjectiveQuestionForm(QuestionForm):
    class Meta:
        model = SubjectiveQuestion
        fields = [
            'expected_answer',
            'key_answers',
        ]
