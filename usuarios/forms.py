from django import forms
from .models import Perfil

class OnboardingForm(forms.ModelForm):
    interesses = forms.MultipleChoiceField(
        choices=Perfil.CATEGORIAS_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=True
    )

    class Meta:
        model = Perfil
        fields = ['interesses']