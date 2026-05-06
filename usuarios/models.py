from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    CATEGORIAS_CHOICES = [
        ('MUSI', 'Música'),
        ('CULT', 'Cultura'),
        ('ESPO', 'Esporte'),
        ('EMPR', 'Empreendedorismo'),
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    interesses = models.JSONField(default=list, blank=True)
    primeiro_acesso = models.BooleanField(default=True)

    def __str__(self):
        return f"Perfil de {self.usuario.username}"