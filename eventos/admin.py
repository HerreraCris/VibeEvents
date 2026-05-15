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
        'data_evento',      # Início (Campo original)
        'data_fim',         # Término (Novo campo)
        'status',           # Moderação (Campo original)
        'status_colorido',  # Bolinhas de moderação
        'situacao_colorida', # US-EV-27: Futuro, Acontecendo, Finalizado
        'is_beneficente'
    )    
    
    list_editable = ('status',)
    list_filter = ('status', 'categoria', 'is_beneficente', 'data_evento', PeriodoFilter)
    search_fields = ('nome', 'nome_local', 'descricao')
    actions = ['aprovar_eventos', 'rejeitar_eventos']

    def nome_formatado(self, obj):
        return format_html('<b>{}</b><br><small style="color:#999">{}</small>', obj.nome, obj.nome_local)
    nome_formatado.short_description = 'Evento / Local'

    # Moderação (PEND, PUBL, REJE)
    def status_colorido(self, obj):
        cores = {
            'PEND': '#ff9800', 
            'PUBL': '#4caf50', 
            'REJE': '#f44336', 
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">● {}</span>',
            cores.get(obj.status, '#ccc'),
            obj.get_status_display()
        )
    status_colorido.short_description = 'Curadoria'

    # NOVO: Lógica da US-EV-27 baseada no tempo
    def situacao_colorida(self, obj):
        situacao = obj.situacao_no_tempo # Chama a property do seu Model
        cores = {
            'FUTURO': '#2196f3',      # Azul
            'ACONTECENDO': '#4caf50', # Verde
            'FINALIZADO': '#9e9e9e',  # Cinza
        }
        cor = cores.get(situacao, '#ccc')
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; border-radius: 10px; font-size: 10px; font-weight: bold;">{}</span>',
            cor,
            situacao
        )
    situacao_colorida.short_description = 'Ciclo de Vida'

    @admin.action(description="🚀 Publicar eventos selecionados")
    def aprovar_eventos(self, request, queryset):
        rows_updated = queryset.update(status='PUBL')
        self.message_user(request, f"{rows_updated} eventos foram publicados com sucesso!")

    @admin.action(description="❌ Rejeitar eventos selecionados")
    def rejeitar_eventos(self, request, queryset):
        rows_updated = queryset.update(status='REJE')
        self.message_user(request, f"{rows_updated} eventos foram marcados como rejeitados.")