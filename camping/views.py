from django.shortcuts import render
from .models import *
# from django.db.models import Q, Prefetch
# from django.views.defaults import page_not_found


# Create your views here.

def index(request):
    return render(request, 'index.html') 

def ver_campings(request):
    campings = Camping.objects.all()
    #campings = (Camping.objects.raw(" SELECT * FROM camping_camping c"))
    
    return render(request, 'URLs/campings.html', {"mostrar_campings":campings})


def ver_reservas_por_fecha(request):
    reservas = Reserva.objects.select_related('cliente__datos_cliente').order_by('fecha_inicio')
    #reservas = (Reserva.objects.raw("SELECT cr.id AS id, cp.nombre, cp.apellido, cr.fecha_inicio, cr.fecha_fin  FROM camping_reserva cr "
    #                                + " JOIN camping_cliente cc ON cr.cliente_id = cc.id "
    #                                + " JOIN camping_persona cp ON cc.id = cp.id "
    #                                "   ORDER BY cr.fecha_inicio"))
    
    return render(request, 'URLs/reservas_fecha.html', {"mostrar_reservas":reservas})


def ver_reserva_por_id(request, id_reserva):
    reserva = Reserva.objects.select_related().prefetch_related().get(id=id_reserva)
    
    reserva = Reserva.objects.raw("SELECT * from camping_reserva"
                                    + "")
    return render(request, 'URLs/reserva_por_id.html', {'mostrar_reserva_por_id':reserva})

