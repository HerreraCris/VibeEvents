from django.shortcuts import render, redirect, get_object_or_404
from django.core.serializers import serialize
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone  
from django.contrib.auth.decorators import login_required 
from datetime import timedelta     
from .models import Evento, Comentario, FotoEvento
from usuarios.models import Perfil
from .forms import EventoCuradoriaForm, ComentarioForm
import json
from rest_framework import generics
from .serializers import EventoSerializer
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import requests
from datetime import datetime

def mapa_eventos(request):
    eventos = Evento.objects.filter(status='PUBL')
    interesses_usuario = []
    periodo = request.GET.get('periodo')
    evento_foco_id = request.GET.get('evento_id') # CAPTURA O ID ENVIADO PELO WHATSAPP (US-EV-21)
    hoje = timezone.now().date()
    
    if request.user.is_authenticated:
        perfil, _ = Perfil.objects.get_or_create(usuario=request.user)
        if perfil.primeiro_acesso:
            return redirect('onboarding') 
        interesses_usuario = perfil.interesses 

    if periodo == 'hoje':
        eventos = eventos.filter(data_evento__date=hoje)
    elif periodo == 'fds':
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
        event_dict['id'] = feature.get('id', str(feature['id']))

        evento_obj = Evento.objects.get(id=feature['id'])
        if evento_obj.imagem_capa:
            event_dict['imagem'] = evento_obj.imagem_capa.url
        else:
            event_dict['imagem'] = '/static/img/default-event.jpg'
            
        comentarios = evento_obj.comentarios.order_by('-criado_em')[:10]
        event_dict['comentarios'] = [
            {
                'usuario': c.usuario.username,
                'texto': c.texto,
                'data': c.criado_em.strftime('%d/%m/%Y %H:%M')
            }
            for c in comentarios
        ]
        simplified_events.append(event_dict)

    context = {
        'eventos_js': simplified_events, 
        'periodo_atual': periodo,
        'interesses_usuario': json.dumps(interesses_usuario),
        'evento_foco_id': evento_foco_id # INJETA NO TEMPLATE PARA O SCRIPT DO LEAFLET CAPTURAR (US-EV-21)
    }
    return render(request, 'eventos/mapa.html', context)
    
@staff_member_required
def cadastrar_evento_curadoria(request):
    if request.method == 'POST':
        form = EventoCuradoriaForm(request.POST, request.FILES)
        if form.is_valid():
            fevento = form.save(commit=False)
            fevento.criado_por = request.user
            fevento.save()
            return redirect('mapa_eventos')
    else:
        form = EventoCuradoriaForm()
    return render(request, 'eventos/curadoria_cadastro.html', {'form': form})

@login_required(login_url='login') 
def sugerir_evento_publico(request):
    if request.method == 'POST':
        form = EventoCuradoriaForm(request.POST, request.FILES)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.status = 'PEND'  
            evento.criado_por = request.user
            evento.save()
            return redirect('sugestao_sucesso')
    else:
        form = EventoCuradoriaForm()
    return render(request, 'eventos/sugerir_evento.html', {'form': form})
    
def sugestao_sucesso(request):
    return render(request, 'eventos/sugestao_sucesso.html')

class EventoListAPIView(generics.ListAPIView):
    queryset = Evento.objects.filter(status='PUBL').order_by('data_evento')
    serializer_class = EventoSerializer

@require_POST
@login_required(login_url='login')
def comentar_evento(request, evento_id):
    evento = Evento.objects.get(id=evento_id)
    texto = request.POST.get('texto', '').strip()

    if not texto:
        return JsonResponse({'erro': 'Comentário não pode estar vazio.'}, status=400)

    palavras_bloqueadas = ['porra', 'caralho', 'merda', 'fdp', 'puta', 'viado', 'bosta', 'desgraça']
    texto_lower = texto.lower()

    for palabra in palavras_bloqueadas:
        if palabra in texto_lower:
            return JsonResponse({'erro': 'Comentário contém linguagem inadequada.'}, status=400)

    Comentario.objects.create(
        evento=evento,
        usuario=request.user,
        texto=texto
    )

    comentarios = evento.comentarios.order_by('-criado_em')[:10]
    data = [
        {
            'usuario': c.usuario.username,
            'texto': c.texto,
            'data': c.criado_em.strftime('%d/%m/%Y %H:%M')
        }
        for c in comentarios
    ]

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'comentarios': data})
    return redirect('detalhe_evento', evento_id=evento.id)

def detalhe_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    comentarios = evento.comentarios.order_by('-criado_em')
    fotos = evento.fotos.order_by('-criado_em')

    pode_enviar_foto = False
    if request.user.is_authenticated:
        if request.user.is_staff or request.user == evento.criado_por:
            pode_enviar_foto = True

    clima = None
    try:
        lat = evento.localizacao.y
        lon = evento.localizacao.x
        api_key = 'e49f82374eef92fa220953b1644f6b2d'
        url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=pt_br'

        response = requests.get(url, timeout=5)
        dados = response.json()
        data_evento = evento.data_evento.date()

        for item in dados['list']:
            dt = datetime.fromtimestamp(item['dt'])
            if dt.date() == data_evento:
                clima = {
                    'temperatura': round(item['main']['temp']),
                    'descricao': item['weather'][0]['description'].capitalize(),
                    'icone': item['weather'][0]['icon']
                }
                break

        if not clima:
            clima = {'erro': 'Sem previsão disponível para essa data.'}
    except Exception as e:
        print("ERRO CLIMA:", e)
        clima = {'erro': 'Não foi possível obter informações sobre o clima.'}

    context = {
        'evento': evento,
        'comentarios': comentarios,
        'fotos': fotos,
        'pode_enviar_foto': pode_enviar_foto,
        'clima': clima
    }
    return render(request, 'eventos/detalhe_evento.html', context)

@login_required(login_url='login')
@require_POST
def upload_foto_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    if not (request.user.is_staff or request.user == evento.criado_por):
        return redirect('detalhe_evento', evento_id=evento.id)

    imagem = request.FILES.get('imagem')
    if imagem:
        FotoEvento.objects.create(
            evento=evento,
            usuario=request.user,
            imagem=imagem
        )
    return redirect('detalhe_evento', evento_id=evento.id)

@login_required(login_url='login')
@require_POST
def alternar_presenca_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    usuario = request.user
    
    if evento.participantes.filter(id=usuario.id).exists():
        evento.participantes.remove(usuario)
        confirmado = False
    else:
        evento.participantes.add(usuario)
        confirmado = True
        
    return JsonResponse({
        'success': True,
        'confirmado': confirmado,
        'total_participantes': evento.total_participantes
    })