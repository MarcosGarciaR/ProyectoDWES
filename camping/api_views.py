from .models import *
from .serializers import * 
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import *

@api_view(['GET'])
def reserva_list(request):

    reservas = Reserva.objects.all()
    serializer = ReservaSerializer(reservas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def reservas_mejoradas_list(request):

    reservas = Reserva.objects.all()
    serializer = ReservaSerializerMejorado(reservas, many=True)
    return Response(serializer.data)






