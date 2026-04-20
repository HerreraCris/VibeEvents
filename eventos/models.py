from django.db import models
from django.contrib.gis.db import models

class Evento(models.Model):
    STATUS_CHOICES = [
        ('PEND', 'Pendente (Análise)'),
        ('PUBL', 'Publicado'),
        ('REJE', 'Rejeitado'),
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
    
    nome_local = models.CharField(max_length=255, verbose_name="Nome do Local (Ex: Teatro, Praça X)", help_text="Nome legível do lugar")

    categoria = models.CharField(
        max_length=4,
        choices=CATEGORIAS_CHOICES,
        default='CULT'
    )

    is_beneficente = models.BooleanField(default=False)
    link_externo = models.URLField(max_length=500)
    localizacao = models.PointField()

    def __str__(self):
        return f"{self.nome} - {self.get_categoria_display()}"
