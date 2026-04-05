
from django.shortcuts import render, redirect
from django.core.serializers import serialize
from django.contrib.admin.views.decorators import staff_member_required
from .models import Evento
from .forms import EventoCuradoriaForm
import json

def mapa_eventos(request):
    # Busca os eventos
    eventos = Evento.objects.all()
    
    # Serializa para GeoJSON (formato que o JS entende nativamente)
    eventos_geojson = serialize('geojson', eventos, geometry_field='localizacao', fields=('nome', 'data_evento', 'is_beneficente', 'link_externo', 'categoria'))
    
    # Converte string GeoJSON para objeto Python para passar ao template
    eventos_data = json.loads(eventos_geojson)
    
    # Simplifica a estrutura para o JS ler mais fácil
    simplified_events = []
    for feature in eventos_data['features']:
        event_dict = feature['properties']
        event_dict['localizacao'] = feature['geometry'] # Inclui a geometria
        simplified_events.append(event_dict)

    return render(request, 'eventos/mapa.html', {'eventos_js': simplified_events})

    
@staff_member_required
def cadastrar_evento_curadoria(request):
    if request.method == 'POST':
        form = EventoCuradoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mapa_eventos') # Volta para o mapa para ver o pin novo
    else:
        form = EventoCuradoriaForm()
    
    return render(request, 'eventos/curadoria_cadastro.html', {'form': form})