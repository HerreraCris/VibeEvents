
from django.shortcuts import render, redirect
from django.core.serializers import serialize
from django.contrib.admin.views.decorators import staff_member_required
from .models import Evento
from .forms import EventoCuradoriaForm
import json

def mapa_eventos(request):
    # Busca todos os eventos cadastrados que estão aprovados
    eventos = Evento.objects.filter(status='aprovado')
    
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

from .forms import EventoPublicoForm
from django.contrib import messages

def sugerir_evento(request):
    if request.method == 'POST':
        form = EventoPublicoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.status = 'pendente'  # 🔥 ESSENCIAL
            evento.save()

            messages.success(request, "Evento enviado para análise!")
            return redirect('mapa_eventos')
    else:
        form = EventoPublicoForm()

    return render(request, 'eventos/sugerir_evento.html', {'form': form})