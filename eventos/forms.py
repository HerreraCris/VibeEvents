from django import forms
from leaflet.forms.widgets import LeafletWidget
from django.contrib.gis.forms import PointField, OSMWidget
from .models import Evento


class EventoCuradoriaForm(forms.ModelForm):
    class Meta:
            model = Evento
            fields = ['nome', 'categoria', 'data_evento', 'link_externo', 'localizacao', 'is_beneficente', 'descricao']
            widgets = {
                'localizacao': LeafletWidget(attrs={
                    'id': 'mapa-curadoria',
                    'style': 'height: 480px; width: 100%;',
                    'data-map-pk': 'mapa-curadoria',
                }),
                'nome': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
                'categoria': forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary'}),
                'data_evento': forms.DateTimeInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'type': 'datetime-local'}),
                'link_externo': forms.URLInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
                'descricao': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 3}),
            }