from django import forms
from .models import Meep


class MeepForm(forms.ModelForm):
    class Meta:
        model = Meep
        fields = ['body']
        widgets = {
            'body': forms.TextInput(attrs={'size': '100'}),
        }
