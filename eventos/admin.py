from django.contrib.gis import admin
from .models import Evento

@admin.register(Evento)
class EventoAdmin(admin.GISModelAdmin):
    # Organização por Seções (Fieldsets) como na imagem enviada
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'categoria', 'link_externo')
        }),
        ('Data & Localização', {
            'fields': ('data_evento', 'localizacao'),
        }),
        ('Descrição Detalhada', {
            'fields': ('descricao', 'is_beneficente'),
        }),
    )

    list_display = ('nome', 'categoria', 'data_evento', 'is_beneficente')
    list_filter = ('categoria', 'is_beneficente')
    
    # Injetando o CSS e JS customizado
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
