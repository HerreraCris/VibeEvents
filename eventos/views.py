
from django.shortcuts import render
from django.core.serializers import serialize
from .models import Evento
import json

def mapa_eventos(request):
    # Busca todos os eventos cadastrados
    eventos = Evento.objects.all()
    
    # Serializa para GeoJSON incluindo o novo campo 'nome_local'
    eventos_geojson = serialize('geojson', eventos, geometry_field='localizacao', 
                                fields=('nome', 'data_evento', 'is_beneficente', 'link_externo', 'categoria' , 'descricao', 'nome_local'))
    
    eventos_data = json.loads(eventos_geojson)
    
    simplified_events = []
    for feature in eventos_data['features']:
        event_dict = feature['properties']
        event_dict['localizacao'] = feature['geometry'] 
        # Adicionamos um ID único para facilitar a manipulação no JS
        event_dict['id'] = feature.get('id', event_dict['nome'].replace(' ', '_'))
        simplified_events.append(event_dict)

    return render(request, 'eventos/mapa.html', {'eventos_js': simplified_events})
