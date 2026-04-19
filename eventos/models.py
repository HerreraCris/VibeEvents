from django.contrib.gis.db import models

class Evento(models.Model):
    CATEGORIAS_CHOICES = [
        ('EMPR', 'Empreendedorismo'),
        ('ESPO', 'Esporte'),
        ('MUSI', 'Música'),
        ('CULT', 'Cultura'),
    ]

    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovado', 'Aprovado'),
        ('rejeitado', 'Rejeitado'),
    ]

    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    data_evento = models.DateTimeField()

    nome_local = models.CharField(
        max_length=255,
        verbose_name="Nome do Local",
        help_text="Ex: Teatro, Praça X"
    )

    categoria = models.CharField(
        max_length=4,
        choices=CATEGORIAS_CHOICES,
        default='CULT'
    )

    is_beneficente = models.BooleanField(default=False)
    link_externo = models.URLField(max_length=500)
    localizacao = models.PointField()

    # 🔥 CORREÇÃO PRINCIPAL
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pendente'
    )

    def __str__(self):
        return f"{self.nome} - {self.get_categoria_display()}"