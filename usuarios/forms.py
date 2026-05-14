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

class PerfilEditForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['interesses'] 
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicando a regra de 44px de altura para facilitar o toque no mobile
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control form-control-lg mb-3',
                'style': 'min-height: 48px;' 
            })