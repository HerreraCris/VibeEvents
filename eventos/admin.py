from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Evento

@admin.register(Evento)
class EventoAdmin(LeafletGeoAdmin):
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
    )

    list_display = ('nome', 'categoria', 'data_evento', 'is_beneficente')
    list_filter = ('categoria', 'is_beneficente')
    
    class Media:
        css = { 'all': ('css/admin_custom.css',) }

    # US-EV-06: Ativa a busca por endereço também no mapa do Admin
    def get_map_widget(self, db_field):
        widget = super().get_map_widget(db_field)
        widget.params['plugins'] = ['geocoder']
        return widget