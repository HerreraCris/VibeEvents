from django.db import models
from django.contrib.gis.db import models as gis_models
from django.utils import timezone

class Evento(models.Model):
    STATUS_CHOICES = [
        ('PEND', 'Pendente (Análise)'),
        ('PUBL', 'Publicado'),
        ('REJE', 'Rejeitado'),
        ('ARQU', 'Arquivado (Passado)'),
    ]

    CATEGORIAS_CHOICES = [
        ('EMPR', 'Empreendedorismo'),
        ('ESPO', 'Esporte'),
        ('MUSI', 'Música'),
        ('CULT', 'Cultura'),
    ]
    status = models.CharField(
        max_length=4,
        choices=STATUS_CHOICES,
        default='PEND',
        verbose_name="Status de Moderação"
    )

    def __str__(self):
        return f"[{self.get_status_display()}] {self.nome}"


    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    data_evento = models.DateTimeField()
    data_fim = models.DateTimeField(verbose_name="Data/Hora de Término", null=True, blank=True)
    
    nome_local = models.CharField(max_length=255, verbose_name="Nome do Local (Ex: Teatro, Praça X)", help_text="Nome legível do lugar")

    categoria = models.CharField(
        max_length=4,
        choices=CATEGORIAS_CHOICES,
        default='CULT'
    )

    is_beneficente = models.BooleanField(default=False)
    link_externo = models.URLField(max_length=500)
    localizacao = gis_models.PointField()
    @property
    def situacao_no_tempo(self):
        """Calcula se o evento é Futuro, Acontecendo ou Finalizado"""
        agora = timezone.now()
        
        if not self.data_fim: # Caso não tenha data fim, consideramos 2h de duração
            data_fim_estimada = self.data_evento + timezone.timedelta(hours=2)
        else:
            data_fim_estimada = self.data_fim

        if agora < self.data_evento:
            return 'FUTURO'
        elif self.data_evento <= agora <= data_fim_estimada:
            return 'ACONTECENDO'
        else:
            return 'FINALIZADO'
    def __str__(self):
        return f"{self.nome} - {self.get_categoria_display()}"

from django.contrib.auth.models import User


class Comentario(models.Model):
    evento = models.ForeignKey(
        Evento,
        on_delete=models.CASCADE,
        related_name='comentarios'
    )

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    texto = models.TextField(max_length=500)

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.evento.nome}"