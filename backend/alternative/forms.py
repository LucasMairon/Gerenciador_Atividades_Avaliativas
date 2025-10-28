from django import forms
from .models import Alternative
from question.templatetags.question_template_utils import decimal_to_letter


class AlternativeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.prefix:
            index = int(self.prefix.split('-')[-1])
            letter = decimal_to_letter(index + 1)
            placeholder_text = f'Digite a alternativa {letter}'
            self.fields['description'].widget.attrs['placeholder'] = placeholder_text

    class Meta:
        model = Alternative
        fields = ['description', 'is_correct']

        widgets = {
            'description': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'rows': 1
                }
            ),
            'is_correct': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input mt-0'
                }
            )
        }
