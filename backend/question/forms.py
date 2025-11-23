from django import forms
from alternative.forms import AlternativeForm
from alternative.models import Alternative
from .models import ObjectiveQuestion, Question, SubjectiveQuestion
from django_summernote.widgets import SummernoteWidget
from django_tomselect.forms import TomSelectModelWidget, TomSelectConfig


class QuestionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        difficulty_level_choices = list(
            self.fields['difficulty_level'].choices)
        difficulty_level_choices.pop(0)

        default_difficulty_choice = [("", 'Selecione a dificuldade')]

        self.fields['difficulty_level'].choices = default_difficulty_choice + \
            difficulty_level_choices

        discipline_choices = list(self.fields['discipline'].choices)
        discipline_choices.pop(0)

        default_discipline_choice = [("", 'Selecione a disciplina')]
        self.fields['discipline'].choices = default_discipline_choice + \
            discipline_choices

    class Meta:
        model = Question
        fields = [
            'statement',
            'difficulty_level',
            'visibility',
            'discipline',
            'subject',
            'topic',
        ]

        widgets = {
            'statement': SummernoteWidget(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Digite o enunciado da questão...',
                }
            ),
            'difficulty_level': forms.Select(
                attrs={
                    'class': 'form-select',
                    'id': 'dificuldade',
                }
            ),
            'visibility':  forms.RadioSelect(
                attrs={
                    'class': 'form-check-input'
                }
            ),
            'discipline': TomSelectModelWidget(
                config=TomSelectConfig(
                    url='discipline:autocomplete',
                    placeholder='Selecione a disciplina',
                    create=False,
                ),
                attrs={
                    'class': 'form-select',
                    'id': 'disciplina',
                    'data-theme': 'bootstrap5',
                }
            ),
            'subject': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'assunto',
                    'placeholder': 'Informe o assunto'
                }
            ),
            'topic': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'topico',
                    'placeholder': 'Informe o tópico'
                }
            )
        }

        labels = {
            'statement': 'Enunciado da questão',
            'difficulty_level': 'Dificuldade',
            'visibility': 'Visibilidade',
            'discipline': 'Disciplina',
            'subject': 'Assunto',
            'topic': 'Tópico'
        }


class ObjectiveQuestionForm(QuestionForm):
    class Meta(QuestionForm.Meta):
        model = ObjectiveQuestion
        fields = QuestionForm.Meta.fields + ['objective',]

        widgets = QuestionForm.Meta.widgets
        widgets.update(
            {
                'objective': forms.Textarea(
                    attrs={
                        'class': 'form-control',
                        'id': 'objetivo',
                        'rows': 3,
                        'placeholder': 'Descreva o objetivo desta questão...'
                    }
                )
            }
        )
        labels = QuestionForm.Meta.labels
        labels.update(
            {
                'objective': 'Objetivo da questão'
            }
        )


QuestionAlternativesFormSet = forms.inlineformset_factory(
    parent_model=ObjectiveQuestion,
    model=Alternative,
    form=AlternativeForm,
    max_num=5,
    min_num=5,
    can_delete=False,
)


class SubjectiveQuestionForm(QuestionForm):
    class Meta(QuestionForm.Meta):
        model = SubjectiveQuestion
        fields = QuestionForm.Meta.fields + [
            'expected_answer',
            'key_answers',
        ]
        widgets = QuestionForm.Meta.widgets.copy()
        labels = QuestionForm.Meta.labels.copy()

        labels.update(
            {
                'expected_answer': 'Resposta esperada',
                'key_answers': 'Palavras-chaves esperadas',
            }
        )

        widgets.update(
            {
                'expected_answer': forms.Textarea(
                    attrs={
                        'class': 'form-control',
                        'id': 'resposta_esperada',
                        'placeholder': 'Descreva a resposta esperada desta questão...',
                        'rows': 5
                    }
                ),
                'key_answers': forms.TextInput(
                    attrs={
                        'class': 'form-control',
                        'id': 'palavras_chave',
                        'placeholder': 'Separe as palavras-chaves por vírgula'
                    }
                )
            }
        )
