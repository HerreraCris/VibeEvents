from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Evento
from django.utils import timezone
from datetime import timedelta
from django.utils.html import format_html

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
    list_display = (
        'nome_formatado', 
        'categoria', 
        'data_evento', 
        'status',          # <--- Adicione o campo real aqui
        'status_colorido',  # Este é o que tem as bolinhas coloridas
        'is_beneficente'
    )
    
    # Agora o Django não vai mais reclamar
    list_editable = ('status',)

    # Filtros laterais para facilitar a vida do moderador
    list_filter = ('status', 'categoria', 'is_beneficente', 'data_evento')
        
    # Busca rápida por nome ou local
    search_fields = ('nome', 'nome_local', 'descricao')

    # Ações em massa: Aprovar ou Rejeitar vários de uma vez
    actions = ['aprovar_eventos', 'rejeitar_eventos']

    # Customização visual do nome para facilitar leitura
    def nome_formatado(self, obj):
        return format_html('<b>{}</b><br><small style="color:#999">{}</small>', obj.nome, obj.nome_local)
    nome_formatado.short_description = 'Evento / Local'

    # Status com cores para o Moderador bater o olho e saber o que falta
    def status_colorido(self, obj):
        cores = {
            'PEND': '#ff9800', # Laranja
            'PUBL': '#4caf50', # Verde
            'REJE': '#f44336', # Vermelho
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">● {}</span>',
            cores.get(obj.status, '#ccc'),
            obj.get_status_display()
        )
    status_colorido.short_description = 'Situação'

    # Lógica das Ações em Massa
    @admin.action(description="🚀 Publicar eventos selecionados")
    def aprovar_eventos(self, request, queryset):
        rows_updated = queryset.update(status='PUBL')
        self.message_user(request, f"{rows_updated} eventos foram publicados com sucesso!")

    @admin.action(description="❌ Rejeitar eventos selecionados")
    def rejeitar_eventos(self, request, queryset):
        rows_updated = queryset.update(status='REJE')
        self.message_user(request, f"{rows_updated} eventos foram marcados como rejeitados.")