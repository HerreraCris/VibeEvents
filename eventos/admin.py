from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Evento
from django.utils import timezone
from datetime import timedelta


class PeriodoFilter(admin.SimpleListFilter):
    title = 'Período do Evento'
    parameter_name = 'periodo'

    def lookups(self, request, model_admin):
        return (
            ('hoje', 'Hoje'),
            ('fds', 'Este Final de Semana'),
            ('7dias', 'Próximos 7 Dias'),
            ('mes', 'Este Mês'),
        )

    def queryset(self, request, queryset):
        hoje = timezone.now().date()
        if self.value() == 'hoje':
            return queryset.filter(data_evento__date=hoje)
        if self.value() == 'fds':
            # Calcula próxima sexta e domingo
            sexta = hoje + timedelta(days=(4 - hoje.weekday()) % 7)
            domingo = sexta + timedelta(days=2)
            return queryset.filter(data_evento__date__range=[sexta, domingo])
        if self.value() == '7dias':
            return queryset.filter(data_evento__date__range=[hoje, hoje + timedelta(days=7)])
        if self.value() == 'mes':
            return queryset.filter(data_evento__month=hoje.month, data_evento__year=hoje.year)

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

    list_display = ('nome', 'categoria', 'data_evento', 'status', 'is_beneficente')
    list_filter = ('status', 'categoria', 'is_beneficente', PeriodoFilter)
    list_editable = ('status',) # Permite aprovar direto na listagem
    search_fields = ('nome', 'descricao')
    
    actions = ['marcar_como_publicado']    
    @admin.action(description="🚀 Publicar eventos selecionados")
    def marcar_como_publicado(self, request, queryset):
        queryset.update(status='PUBL')


    class Media:
        css = { 'all': ('css/admin_custom.css',) }

    # US-EV-06: Ativa a busca por endereço também no mapa do Admin
    def get_map_widget(self, db_field):
        widget = super().get_map_widget(db_field)
        widget.params['plugins'] = ['geocoder']
        return widget