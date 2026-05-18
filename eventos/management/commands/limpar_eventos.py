# eventos/management/commands/limpar_eventos.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from eventos.models import Evento

class Command(BaseCommand):
    help = 'Arquiva eventos que terminaram há mais de 24 horas'

    def handle(self, *args, **options) :
        # Define o limite: agora menos 24 horas
        limite = timezone.now() - timedelta(hours=24)
        
        # Filtra eventos que:
        # 1. Têm data_fim anterior ao limite
        # 2. Ou não têm data_fim, mas a data_evento (início) + 2h é anterior ao limite
        
        # Eventos com data_fim definida
        eventos_com_fim = Evento.objects.filter(
            data_fim__lt=limite,
            status='PUBL'
        )
        
        # Eventos sem data_fim (usando a lógica de 2h de duração estimada)
        limite_sem_fim = timezone.now() - timedelta(hours=26) # 24h + 2h de duração
        eventos_sem_fim = Evento.objects.filter(
            data_fim__isnull=True,
            data_evento__lt=limite_sem_fim,
            status='PUBL'
        )

        total_com_fim = eventos_com_fim.count()
        total_sem_fim = eventos_sem_fim.count()

        # Executa a "Faxina": alterando para um status de arquivado ou removendo o 'PUBL'
        eventos_com_fim.update(status='ARQU') # Ou 'ARQU' se você criar esse status
        eventos_sem_fim.update(status='ARQU')

        self.stdout.write(
            self.style.SUCCESS(f'Faxina concluída: {total_com_fim + total_sem_fim} eventos arquivados.')
        )