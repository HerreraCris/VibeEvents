from django.shortcuts import render, redirect
from django.core.serializers import serialize
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone   
from datetime import timedelta     
from .models import Evento
from .forms import EventoCuradoriaForm
import json

def mapa_eventos(request):
    eventos = Evento.objects.filter(status='PUBL')
    periodo = request.GET.get('periodo')
    hoje = timezone.now().date()

    if periodo == 'hoje':
        eventos = eventos.filter(data_evento__date=hoje)
    elif periodo == 'fds':
        # Calcula a próxima sexta-feira (4) e o domingo seguinte
        sexta = hoje + timedelta(days=(4 - hoje.weekday()) % 7)
        eventos = eventos.filter(data_evento__date__range=[sexta, sexta + timedelta(days=2)])
    elif periodo == '7dias':
        eventos = eventos.filter(data_evento__date__range=[hoje, hoje + timedelta(days=7)])

    eventos = eventos.order_by('data_evento')

    eventos_geojson = serialize('geojson', eventos, geometry_field='localizacao', 
                                fields=('nome', 'data_evento', 'is_beneficente', 'link_externo', 'categoria' , 'descricao', 'nome_local'))
    
    eventos_data = json.loads(eventos_geojson)
    
    simplified_events = []
    for feature in eventos_data['features']:
        event_dict = feature['properties']
        event_dict['localizacao'] = feature['geometry'] 
        event_dict['id'] = feature.get('id', event_dict['nome'].replace(' ', '_'))
        simplified_events.append(event_dict)

    context = {
        'eventos_js': simplified_events, 
        'periodo_atual': periodo
    }
    
    
    return render(request, 'eventos/mapa.html', context)

@staff_member_required
def cadastrar_evento_curadoria(request):
    if request.method == 'POST':
        form = EventoCuradoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mapa_eventos')
    else:
        form = EventoCuradoriaForm()
    
    return render(request, 'eventos/curadoria_cadastro.html', {'form': form})

def sugerir_evento_publico(request):
    if request.method == 'POST':
        form = EventoCuradoriaForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.status = 'PEND'  # Força o status pendente para segurança
            evento.save()
            return redirect('sugestao_sucesso')
    else:
        form = EventoCuradoriaForm()
    
    return render(request, 'eventos/sugerir_evento.html', {'form': form})

    
def sugestao_sucesso(request):
    return render(request, 'eventos/sugestao_sucesso.html')