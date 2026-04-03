
from django.shortcuts import render
from django.core.serializers import serialize
from .models import Evento
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
