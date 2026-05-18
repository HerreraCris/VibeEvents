from django.urls import path
from . import views
from .views import EventoListAPIView

urlpatterns = [
    path('', views.mapa_eventos, name='mapa_eventos'),
    path('sugerir/', views.sugerir_evento_publico, name='sugerir_evento'), 
    path('curadoria/novo/', views.cadastrar_evento_curadoria, name='curadoria_novo'),
    path('sugestao-enviada/', views.sugestao_sucesso, name='sugestao_sucesso'),
    path('api/eventos/', EventoListAPIView.as_view(), name='api-eventos-list'),
    
    # Linha corrigida aqui embaixo:
    path('evento/<int:evento_id>/', views.detalhe_evento, name='detalhe_evento'),
    
    path('evento/<int:evento_id>/foto/', views.upload_foto_evento, name='upload_foto_evento'),
    path('evento/<int:evento_id>/comentar/', views.comentar_evento, name='comentar_evento'),
    path('evento/<int:evento_id>/presenca/', views.alternar_presenca_evento, name='alternar_presenca_evento'),
]