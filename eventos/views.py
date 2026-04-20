from django.shortcuts import render, redirect
from django.core.serializers import serialize
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone  # IMPORTANTE: Adicionado
from datetime import timedelta     # IMPORTANTE: Adicionado
from .models import Evento
from .forms import EventoCuradoriaForm
import json

def mapa_eventos(request):
    # 1. Captura o filtro da URL (Ex: ?periodo=hoje)
    periodo = request.GET.get('periodo')
    eventos = Evento.objects.all()
    hoje = timezone.now().date()

    # 2. Lógica de filtragem profissional
    if periodo == 'hoje':
        eventos = eventos.filter(data_evento__date=hoje)
    elif periodo == 'fds':
        # Calcula a próxima sexta-feira (4) e o domingo seguinte
        sexta = hoje + timedelta(days=(4 - hoje.weekday()) % 7)
        eventos = eventos.filter(data_evento__date__range=[sexta, sexta + timedelta(days=2)])
    elif periodo == '7dias':
        eventos = eventos.filter(data_evento__date__range=[hoje, hoje + timedelta(days=7)])

    # 3. Ordenação (Sempre os mais próximos primeiro)
    eventos = eventos.order_by('data_evento')

    # 4. Serialização para GeoJSON (Mantendo sua estrutura original)
    eventos_geojson = serialize('geojson', eventos, geometry_field='localizacao', 
                                fields=('nome', 'data_evento', 'is_beneficente', 'link_externo', 'categoria' , 'descricao', 'nome_local'))
    
    eventos_data = json.loads(eventos_geojson)
    
    simplified_events = []
    for feature in eventos_data['features']:
        event_dict = feature['properties']
        event_dict['localizacao'] = feature['geometry'] 
        event_dict['id'] = feature.get('id', event_dict['nome'].replace(' ', '_'))
        simplified_events.append(event_dict)

    # 5. Retorno único para o template
    return render(request, 'eventos/mapa.html', {
        'eventos_js': simplified_events, 
        'periodo_atual': periodo
    })

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