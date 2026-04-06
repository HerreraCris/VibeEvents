
from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Evento

@admin.register(Evento)
class EventoAdmin(LeafletGeoAdmin): 
    # Campos que aparecem na lista de eventos
    list_display = ('nome', 'categoria', 'data_evento', 'is_beneficente', 'nome_local')
    
    # Filtros na lateral direita
    list_filter = ('categoria', 'is_beneficente', 'data_evento')
    
    # Barra de busca por texto (para o nome ou descrição)
    search_fields = ('nome', 'descricao', 'nome_local')

    # Configurações do mapa no formulário de cadastro
    settings_overrides = {
        'DEFAULT_CENTER': [-10.18, -48.33],
        'DEFAULT_ZOOM': 13,
    }

    # Esta função adiciona o buscador de endereço (Lupa) no mapa do Admin
    def get_inline_instances(self, request, obj=None):
        return super().get_inline_instances(request, obj)