from rest_framework import serializers
from .models import Evento, Comentario

class EventoSerializer(serializers.ModelSerializer):
    categoria_display = serializers.CharField(source='get_categoria_display', read_only=True)
    
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()

    class Meta:
        model = Evento
        fields = [
            'id', 'nome', 'descricao', 'data_evento', 
            'categoria', 'categoria_display', 'is_beneficente', 
            'latitude', 'longitude', 'link_externo', 'status'
        ]

    def get_latitude(self, obj):
        return obj.localizacao.y if obj.localizacao else None

    def get_longitude(self, obj):
        return obj.localizacao.x if obj.localizacao else None