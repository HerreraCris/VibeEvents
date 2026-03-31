from django.contrib.gis import admin
from .models import Evento

@admin.register(Evento)
class EventoAdmin(admin.GISModelAdmin): 
    list_display = ('nome', 'categoria', 'data_evento', 'is_beneficente')
    list_filter = ('categoria', 'is_beneficente')
    search_fields = ('nome', 'descricao')
