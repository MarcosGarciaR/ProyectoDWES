from django.shortcuts import render
from .models import *
from django.db.models import Avg, Max, Min, Q
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
    """
    reservas = (Reserva.objects.raw("SELECT cr.id AS id, cp.nombre, cp.apellido, cr.fecha_inicio, cr.fecha_fin  FROM camping_reserva cr "
                                    + " JOIN camping_cliente cc ON cr.cliente_id = cc.id "
                                    + " JOIN camping_persona cp ON cc.id = cp.id "
                                    "   ORDER BY cr.fecha_inicio"))
    """
    return render(request, 'URLs/reservas_fecha.html', {"mostrar_reservas":reservas})


def ver_reserva_por_id(request, id_reserva):
    reserva = Reserva.objects.select_related('cliente__datos_cliente').prefetch_related("actividades").get(id=id_reserva)
    
    """
    reserva = Reserva.objects.raw("SELECT cr.id, cr.fecha_inicio, cr.fecha_fin, cp.nombre, cact.* from camping_reserva cr"
                                    + "JOIN camping_camping_cliente cc ON cr.cliente_id = cc.id "
                                    + "JOIN camping_persona cp ON cc.id = cp.id "
                                    + "JOIN camping_reserva_actividades cra ON cra.reserva_id= cr.id "
                                    + "JOIN camping_actividad cact ON cra.actividad_id = cact.id"
                                    + "WHERE cr.id = id_reserva")
    """
    
    return render(request, 'URLs/reserva_por_id.html', {'mostrar_reservaid':reserva})


#   Hacer filtro AND con precio de factura >= 'X' y capacidad de personas de la Parcela >= Y
def ver_factura_precio_capacidad(request, precio, capacidadParcela):
    facturas = Factura.objects.select_related('reserva__reserva__parcela').filter(total__gte=precio, reserva__reserva__parcela__capacidad__gte=capacidadParcela)
    
    """
    facturas = Factura.objects.raw("SELECT * FROM camping_factura cf"
                                    + "JOIN camping_reservaextra cre ON cf.reserva_id = cre.id"
                                    + "JOIN camping_reserva cr ON cre.reserva_id = cr.id"
                                    + "JOIN camping_parcela cp ON cr.parcela_id = cp.id"
                                    + "WHERE cf.total > precio AND cp.capacidad > capacidadParcela")
    """
    return render(request, 'URLs/factura_precio_capacidad.html',{'mostrar_facturas':facturas})


#   URL con la media de precios de los servicios
def precio_medio_servicios(request):
    servicios = ServiciosExtra.objects.aggregate(Avg("precio"),Max("precio"),Min("precio"))
    
    media = servicios["precio__avg"]
    maximo = servicios["precio__max"] 
    minimo = servicios["precio__min"]
    return render(request, 'URLs/servicios_media_puntos.html',{"media":media, "maximo":maximo, "minimo":minimo})


#   Hacer filtro OR con las puntuaciones de los cuidadores, > X o esté disponible de noche
def puntuacionydisponibilidad_cuidadores(request, puntuacionPedida):
    cuidadores = Cuidador.objects.select_related('usuario__datos_usuario').filter(Q(puntuacion__gt=puntuacionPedida) | Q(disponible_de_noche=True) )
    return render(request, 'URLs/puntuacionydisponibilidad_cuidadores.html', {'mostrar_cuidadores':cuidadores})
