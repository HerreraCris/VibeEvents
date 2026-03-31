from django.db import models

# Create your models here.

from django.contrib.gis.db import models

class Evento(models.Model):
    CATEGORIAS_CHOICES = [
        ('EMPR', 'Empreendedorismo'),
        ('ESPO', 'Esporte'),
        ('MUSI', 'Música'),
        ('CULT', 'Cultura'),
    ]

    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    data_evento = models.DateTimeField()

    # Campo para filtrar por categoria [cite: 137]
    categoria = models.CharField(
        max_length=4,
        choices=CATEGORIAS_CHOICES,
        default='CULT'
    )

    # Diferenciação visual para o "Selo Evento Solidário" [cite: 125, 138]
    is_beneficente = models.BooleanField(default=False)

    # Link para inscrição em plataformas externas (Sympla/WhatsApp) [cite: 113, 131]
    link_externo = models.URLField(max_length=500)

    # O "Pin" no mapa para geolocalização [cite: 96, 118]
    localizacao = models.PointField()

    def __str__(self):
        return f"{self.nome} - {self.get_categoria_display()}"


