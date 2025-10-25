from django.shortcuts import render
from .models import *
from django.db.models import Avg, Max, Min, Q, Prefetch
# from django.views.defaults import page_not_found


# Create your views here.

def index(request):
    return render(request, 'index.html') 

#   Ver la lista de campings
def ver_campings(request):
    campings = Camping.objects.all()
    
    """
    campings = (Camping.objects.raw(" SELECT * FROM camping_camping c"))
    """
    
    return render(request, 'URLs/campings.html', {"mostrar_campings":campings})

#   Ordenar las reservas por fecha de inicio
def ver_reservas_por_fecha(request):
    reservas = Reserva.objects.select_related('cliente__datos_cliente').order_by('fecha_inicio')
    
    """
    reservas = (Reserva.objects.raw("SELECT cr.id AS id, cp.nombre, cp.apellido, cr.fecha_inicio, cr.fecha_fin  FROM camping_reserva cr "
                                    + " JOIN camping_cliente cc ON cr.cliente_id = cc.id "
                                    + " JOIN camping_persona cp ON cc.id = cp.id "
                                    "   ORDER BY cr.fecha_inicio"))
    """
    
    return render(request, 'URLs/reservas_fecha.html', {"mostrar_reservas":reservas})


#   Ver la reserva cuyo ID se pasa por la URL
def ver_reserva_por_id(request, id_reserva):
    reserva = Reserva.objects.select_related('cliente__datos_cliente').prefetch_related("actividades").get(id=id_reserva)
    
    """
    reserva = Reserva.objects.raw("SELECT cr.id, cr.fecha_inicio, cr.fecha_fin, cp.nombre, cact.* from camping_reserva cr"
                                    + "JOIN camping_camping_cliente cc ON cr.cliente_id = cc.id "
                                    + "JOIN camping_persona cp ON cc.id = cp.id "
                                    + "JOIN camping_reserva_actividades cra ON cra.reserva_id= cr.id "
                                    + "JOIN camping_actividad cact ON cra.actividad_id = cact.id"
                                    + "WHERE cr.id = %s", [id_reserva])[0]
    """
    
    return render(request, 'URLs/reserva_por_id.html', {'mostrar_reservaid':reserva})


#   Mostrar las facturas mediante el uso de un filtro AND con precio de factura >= 'X' y capacidad de personas de la Parcela >= Y
def ver_factura_precio_capacidad(request, precio, capacidadParcela):
    facturas = Factura.objects.select_related('reserva__reserva__parcela').filter(total__gte=precio, reserva__reserva__parcela__capacidad__gte=capacidadParcela)
    
    """
    facturas = Factura.objects.raw("SELECT * FROM camping_factura cf"
                                    + "JOIN camping_reservaextra cre ON cf.reserva_id = cre.id"
                                    + "JOIN camping_reserva cr ON cre.reserva_id = cr.id"
                                    + "JOIN camping_parcela cp ON cr.parcela_id = cp.id"
                                    + "WHERE cf.total > %s AND cp.capacidad > %s", [int(precio),int(capacidadParcela)])
    """
    
    return render(request, 'URLs/factura_precio_capacidad.html',{'mostrar_facturas':facturas})


#   URL con la media de precios de los servicios
def precio_medio_servicios(request):
    servicios = ServiciosExtra.objects.aggregate(Avg("precio"),Max("precio"),Min("precio"))
    media = servicios["precio__avg"]
    maximo = servicios["precio__max"] 
    minimo = servicios["precio__min"]    
    
    """
    servicios = ServiciosExtra.objects.raw("SELECT AVG(precio), MAX(precio), MIN(precio) FROM camping_serviciosextra")
    """
    
    return render(request, 'URLs/servicios_media_puntos.html',{"media":media, "maximo":maximo, "minimo":minimo})


#   Mostrar los cuidadores mediante un filtro OR con las puntuaciones de los cuidadores, > X o esté disponible de noche
def puntuacionydisponibilidad_cuidadores(request, puntuacionPedida):
    cuidadores = Cuidador.objects.select_related('usuario__datos_usuario').filter(Q(puntuacion__gt=puntuacionPedida) | Q(disponible_de_noche=True) )
    
    """
    cuidadores = Cuidador.objects.raw("Select * FROM camping_cuidador cc"
                                        + "JOIN camping_perfilusuario cpu ON cc.usuario_id = cpu.id"
                                        + "JOIN camping_persona cp ON cpu.datos_usuario.id = cp.id"
                                        + "WHERE cc.puntuacion > %s OR cc.disponible_de_noche", [int(puntuacionPedida)])
    """
    
    return render(request, 'URLs/puntuacionydisponibilidad_cuidadores.html', {'mostrar_cuidadores':cuidadores})


#   Busqueda de ServiciosExtra cuya descripción tenga la palabra recibida por parámetro.
def busqueda_descripcion_serviciosextra(request, texto):
    servicios = ServiciosExtra.objects.filter(descripcion__contains=texto)
    
    """
    textoDescripcion = "'%"+texto+"%'"
    servicios = ServiciosExtra.objects.raw("SELECT * FROM camping_serviciosextra cse "
                                            + "WHERE cse.descripcion LIKE %s", [textoDescripcion])
    """
    
    return render(request, 'URLs/servicios_extra_descripcion.html', {'mostrar_servicios':servicios})


#   URL con filtro none CLIENTES que no aparecen en la tabla intermedia VEHICULO_CLIENTE
def clientes_sin_vehiculo(request):
    clientes = Cliente.objects.select_related('datos_cliente').prefetch_related(Prefetch("vehiculos")).filter(vehiculos__isnull=True)
    
    """
    clientes = Cliente.objects.raw("SELECT * FROM camping_cliente cc"
                                    + "WHERE cc.id NOT IN ("SELECT cliente_id FROM camping_vehiculo_cliente")")
    """
    
    return render(request, 'URLs/clientes_sin_vehiculo.html', {'mostrar_clientes_sin_vehiculo':clientes})


#   Mostrar las reservas que no tienen actividades asociadas
def reservas_sin_actividades(request):
    reservas = Reserva.objects.select_related("cliente__datos_cliente").prefetch_related(Prefetch("actividades")).filter(actividades__isnull=True).order_by('id')[:10]
    
    """
    reservas = Reserva.objects.raw("SELECT * FROM camping_reserva cr"
                                    + "WHERE cr.id NOT IN ("SELECT reserva_id FROM camping_reserva_actividades")")
    """
    
    return render(request, 'URLs/reservas_sin_actividades.html', {'mostrar_reservas':reservas})


#   Ver las reservas que ha realizado un cliente.
def reservas_de_cliente_por_id(request, cliente_id):
    cliente = Cliente.objects.select_related('datos_cliente') .prefetch_related("reservas").get(id=cliente_id)
    return render(request, 'URLs/reservas_cliente.html', {'cliente': cliente})