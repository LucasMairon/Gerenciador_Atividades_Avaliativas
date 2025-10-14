from django import forms
from .models import Alternative


class AlternativeForm(forms.ModelForm):
    class Meta:
        model = Alternative
        fields = ['description', 'is_correct']
