from django.contrib import admin
from django.contrib.gis import admin as gis_admin 
from .models import Evento

@admin.register(Evento)
class EventoAdmin(gis_admin.GISModelAdmin):
    # Organização por Seções (Fieldsets)
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'categoria', 'link_externo')
        }),
        ('Data & Localização', {
            'fields': ('data_evento', 'nome_local', 'localizacao'), # Adicionado nome_local aqui
        }),
        ('Descrição Detalhada', {
            'fields': ('descricao', 'is_beneficente'),
        }),
    )

    list_display = ('nome', 'categoria', 'data_evento', 'is_beneficente')
    list_filter = ('categoria', 'is_beneficente')
    
    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }

    # Configuração do Mapa
    gis_widget_kwargs = {
        'attrs': {
            'default_zoom': 13,
            'default_lon': -48.33,
            'default_lat': -10.18,
        }
    }