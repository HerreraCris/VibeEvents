
from django.urls import path
from . import views

urlpatterns = [
    path('', views.mapa_eventos, name='mapa_eventos'),
    path('sugerir/', views.sugerir_evento_publico, name='sugerir_evento'), 
    path('curadoria/novo/', views.cadastrar_evento_curadoria, name='curadoria_novo'),
    path('sugestao-enviada/', views.sugestao_sucesso, name='sugestao_sucesso'),
]