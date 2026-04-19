from django.contrib import admin
from django.contrib.gis import admin as gis_admin 
from .models import Evento

@admin.register(Evento)
class EventoAdmin(gis_admin.GISModelAdmin):

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'categoria', 'link_externo')
        }),
        ('Data & Localização', {
            'fields': ('data_evento', 'nome_local', 'localizacao'),
        }),
        ('Descrição Detalhada', {
            'fields': ('descricao', 'is_beneficente'),
        }),
        ('Moderação', {  # 🔥 NOVO
            'fields': ('status',),
        }),
    )

    list_display = ('nome', 'categoria', 'data_evento', 'status', 'is_beneficente')  # 🔥 ADD status
    list_filter = ('categoria', 'is_beneficente', 'status')  # 🔥 ADD status
    
    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }

    gis_widget_kwargs = {
        'attrs': {
            'default_zoom': 13,
            'default_lon': -48.33,
            'default_lat': -10.18,
        }
    }