from rest_framework import serializers
from .models import *

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = '__all__'


class ActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class ParcelaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcela
        fields = '__all__'


class ReservaSerializerMejorado(serializers.ModelSerializer):
    cliente = ClienteSerializer()
    
    parcela = ParcelaSerializer()
    
    fecha_inicio = serializers.DateField(format="%d-%m-%Y")
    
    fecha_fin = serializers.DateField(format="%d-%m-%Y")
    
    actividades = ActividadSerializer(many=True, read_only=True)
    
    class Meta:
        model = Reserva
        fields = '__all__'









