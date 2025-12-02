from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.db.models import Avg, Max, Min, Q, Prefetch
from django.views.defaults import page_not_found
from django.contrib import messages


# Create your views here.

def index(request):
    return render(request, 'index.html') 

#   Ver la lista de campings
def ver_campings(request):
    campings = Camping.objects.all()
    
    """
    campings = (Camping.objects.raw(" SELECT * FROM camping_camping c"))
    """
    
    return render(request, 'URLs/campings/lista_campings.html', {"mostrar_campings":campings})

#   Ordenar las reservas por fecha de inicio
def ver_reservas_por_fecha(request):
    reservas = Reserva.objects.select_related('cliente__datos_cliente','parcela__camping').order_by('fecha_inicio').all()

    """
    reservas = (Reserva.objects.raw("SELECT cr.id AS id, cp.nombre, cp.apellido, cr.fecha_inicio, cr.fecha_fin  FROM camping_reserva cr "
                                    + " JOIN camping_cliente cc ON cr.cliente_id = cc.id "
                                    + " JOIN camping_persona cp ON cc.id = cp.id "
                                    "   ORDER BY cr.fecha_inicio"))
    """
    
    return render(request, 'URLs/reservas/reservas_fecha.html', {"mostrar_reservas":reservas})


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
    cliente = reserva.cliente
    return render(request, 'URLs/reservas/reserva_por_id.html', {'reserva':reserva, 'cliente':cliente})


#   Mostrar las facturas mediante el uso de un filtro AND con precio de factura >= 'X' y capacidad de personas de la Parcela >= Y
def ver_factura_precio_capacidad(request, precio, capacidadParcela):
    facturas = Factura.objects.select_related('reserva_extra__reserva_asociada__parcela').filter(total__gte=precio, reserva_extra__reserva_asociada__parcela__capacidad__gte=capacidadParcela).all()
    
    """
    facturas = Factura.objects.raw("SELECT * FROM camping_factura cf"
                                    + "JOIN camping_reservaextra cre ON cf.reserva_id = cre.id"
                                    + "JOIN camping_reserva cr ON cre.reserva_id = cr.id"
                                    + "JOIN camping_parcela cp ON cr.parcela_id = cp.id"
                                    + "WHERE cf.total > %s AND cp.capacidad > %s", [int(precio),int(capacidadParcela)])
    """
    
    return render(request, 'URLs/facturas/factura_precio_capacidad.html',{'mostrar_facturas':facturas})


#   URL con la media de precios de los servicios
def precio_medio_servicios(request):
    servicios = ServiciosExtra.objects.aggregate(Avg("precio"),Max("precio"),Min("precio"))
    
    """AGREGAR ALL
        servicios = ServiciosExtra.objects. 
    """
    media = servicios["precio__avg"]
    maximo = servicios["precio__max"] 
    minimo = servicios["precio__min"]
    
    """
    servicios = ServiciosExtra.objects.raw("SELECT AVG(precio), MAX(precio), MIN(precio) FROM camping_serviciosextra")
    """
    
    return render(request, 'URLs/serviciosExtra/servicios_media_puntos.html',{"media":media, "maximo":maximo, "minimo":minimo})


#   Mostrar los cuidadores mediante un filtro OR con las puntuaciones de los cuidadores, > X o esté disponible de noche
def puntuacionydisponibilidad_cuidadores(request, puntuacionPedida):
    cuidadores = Cuidador.objects.select_related('usuario__datos_usuario').filter(Q(puntuacion__gt=puntuacionPedida) | Q(disponible_de_noche=True)).all()
    
    """
    cuidadores = Cuidador.objects.raw("Select * FROM camping_cuidador cc"
                                        + "JOIN camping_perfilusuario cpu ON cc.usuario_id = cpu.id"
                                        + "JOIN camping_persona cp ON cpu.datos_usuario.id = cp.id"
                                        + "WHERE cc.puntuacion > %s OR cc.disponible_de_noche", [int(puntuacionPedida)])
    """
    
    return render(request, 'URLs/cuidadores/puntuacionydisponibilidad_cuidadores.html', {'mostrar_cuidadores':cuidadores})


#   Busqueda de ServiciosExtra cuya descripción tenga la palabra recibida por parámetro.
def busqueda_descripcion_serviciosextra(request, texto):
    servicios = ServiciosExtra.objects.filter(descripcion__contains=texto).all()
    
    """
    textoDescripcion = "'%"+texto+"%'"
    servicios = ServiciosExtra.objects.raw("SELECT * FROM camping_serviciosextra cse "
                                            + "WHERE cse.descripcion LIKE %s", [textoDescripcion])
    """
    
    return render(request, 'URLs/serviciosExtra/servicios_extra_descripcion.html', {'mostrar_servicios':servicios})


#   URL con filtro none CLIENTES que no aparecen en la tabla intermedia VEHICULO_CLIENTE
def clientes_sin_vehiculo(request):
    clientes = Cliente.objects.select_related('datos_cliente').filter(vehiculos=None).all()
    
    """
    clientes = Cliente.objects.raw("SELECT * FROM camping_cliente cc"
                                    + "WHERE cc.id NOT IN ("SELECT cliente_id FROM camping_vehiculo_cliente")")
    """
    
    return render(request, 'URLs/clientes/clientes_sin_vehiculo.html', {'mostrar_clientes_sin_vehiculo':clientes})


#   Mostrar las reservas que no tienen actividades asociadas
def reservas_sin_actividades(request):
    reservas = Reserva.objects.select_related("cliente__datos_cliente").prefetch_related(Prefetch("actividades")).filter(actividades=None).order_by('id')[:10].all()
    
    """
    reservas = Reserva.objects.raw("SELECT * FROM camping_reserva cr"
                                    + "WHERE cr.id NOT IN ("SELECT reserva_id FROM camping_reserva_actividades")")
    """
    
    return render(request, 'URLs/reservas/reservas_sin_actividades.html', {'mostrar_reservas':reservas})


#   Ver las reservas que ha realizado un cliente.
def reservas_de_cliente_por_id(request, cliente_id):
    cliente = Cliente.objects.select_related('datos_cliente') .prefetch_related("reservas").get(id=cliente_id)
    
    """
    cliente = Cliente.objects.raw("SELECT * FROM camping_cliente cc"
                                    + "JOIN camping_datos_cliente cdc ON c.datos_cliente_id = cdc.id"
                                    + "JOIN camping_reserva cr ON cr.cliente_id = cc.id"
                                    + "WHERE c.id = %s", [cliente_id])
    """
    
    return render(request, 'URLs/reservas/reservas_cliente.html', {'cliente': cliente})


#   PÁGINAS DE ERRORES
def mi_error_404(request, exception=None):
    return render(request, 'Errores/404.html',None,None,404)

def mi_error_400(request, exception=None):
    return render(request, 'Errores/400.html',None,None,400)

def mi_error_403(request, exception=None):
    return render(request, 'Errores/403.html',None,None,403)

def mi_error_500(request, exception=None):
    return render(request, 'Errores/500.html',None,None,500)



# PRUEBA DE CLASE

def prueba_clase(request):
    #recepcionistas = Persona.objects.all().filter(salario = 1968.15 ).filter( turno = 'ma' )
    
    #recepcionistas = Persona.objects.select_related('usuario_id').all()
    recepcionistas = Recepcionista.objects.raw(" SELECT * FROM camping_recepcionista cr "
    #                                            + "WHERE cr.salario = 1968.15 AND cr.turno = 'ma' "
                                                + "JOIN camping_perfilusuario cpu ON cr.usuario_id = cpu.id ")
    return render(request, 'URLs/recepcionistas/recepcionistas.html', {'recepcionistas':recepcionistas})


#   Ver la lista de personas
def ver_personas(request):
    personas = Persona.objects.all()
    
    """
    personas = (Persona.objects.raw(" SELECT * FROM camping_persona p"))
    """
    
    return render(request, 'URLs/personas/lista_personas.html', {"mostrar_personas":personas})

"""=================================================================================FORMULARIOS========================================================================================================================="""

# PERSONA
## CREATE
def crear_persona(request):
    datosFormulario = None
    if(request.method == 'POST'):
        datosFormulario = request.POST
    formulario = PersonaModelForm(datosFormulario)
    
    if(request.method == "POST"):
        persona_creado = crear_persona_modelo(formulario)
        if(persona_creado):
            messages.success(request, "Se ha creado la persona con nombre "+formulario.cleaned_data.get('nombre')+ " correctamente")
            return redirect("ver_personas")
                
    return render(request, 'URLs/personas/create.html', {'formulario':formulario})

def crear_persona_modelo(formulario):
    persona_creado=False
    if formulario.is_valid():
        try:
            formulario.save()
            persona_creado = True
        except Exception as error:
            print(error)
    
    return persona_creado


## READ
def buscar_personas(request):
    formulario = BusquedaPersonasForm(request.GET)
    
    if(len(request.GET) > 0):
        formulario = BusquedaPersonasForm(request.GET)
        
        if formulario.is_valid():
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"
            
            # QUERY SETS AQUI
            QSpersonas = Persona.objects
            
            nombreBusqueda = formulario.cleaned_data.get('nombreBusqueda')
            apellidosBusqueda = formulario.cleaned_data.get('apellidosBusqueda')
            dni = formulario.cleaned_data.get('dni')
            annio_nacimiento = formulario.cleaned_data.get('annio_nacimiento')
            
            if(nombreBusqueda != ""):
                QSpersonas = QSpersonas.filter(nombre__contains=nombreBusqueda)
                mensaje_busqueda += "Nombre con contenido: "+nombreBusqueda + "\n"
            
            if(apellidosBusqueda != ""):
                QSpersonas = QSpersonas.filter(apellido__contains=apellidosBusqueda)
                mensaje_busqueda += "Apellido con contenido: "+apellidosBusqueda + "\n"
            
            if(dni != ""):
                QSpersonas = QSpersonas.filter(dni__contains=dni)
                mensaje_busqueda += "Con DNI: "+dni + "\n"
            
            if(annio_nacimiento != None ):
                QSpersonas = QSpersonas.filter(fecha_nacimiento__year= annio_nacimiento)
                mensaje_busqueda += "Con año de nacimiento: "+annio_nacimiento
            
            personas = QSpersonas.all()
            return render(request, 'URLs/personas/lista_personas.html', {'mostrar_personas':personas, "texto_busqueda":mensaje_busqueda})

    else:
        formulario = BusquedaPersonasForm(None)
    
    return render(request, 'URLs/personas/busqueda_avanzada.html', {'formulario':formulario})


## UPDATE
def persona_editar(request, persona_id):
    persona = Persona.objects.get(id = persona_id)
    datosFormulario = None
    
    if(request.method == 'POST'):
        datosFormulario = request.POST
    formulario = PersonaModelForm(datosFormulario, instance = persona)
    
    
    if(request.method == "POST"):
        if formulario.is_valid():
            try:
                formulario.save()
                messages.success(request, 'Se ha editado la persona '+formulario.cleaned_data.get('dni')+" correctamente")
                return redirect('ver_personas')
            except Exception as e:
                print(e)
    
    return render(request, 'URLs/personas/actualizar.html', {'formulario':formulario, 'persona':persona})


## DELETE
def persona_eliminar(request, persona_id):
    persona = Persona.objects.get(id = persona_id)
    try:
        persona.delete()
    except Exception as e:
        print(e)
    
    return redirect('ver_personas')


"""=================================================================================PERFILES DE USUARIO========================================================================================================================="""
def ver_perfiles(request):
    perfiles = PerfilUsuario.objects.select_related('datos_usuario').all()
    
    return render(request, 'URLs/perfilesUsuario/lista_perfiles.html', {'mostrar_perfiles':perfiles})

## CREATE
def crear_perfil_usuario(request):
    
    """
    En caso de no haber ninguna persona sin perfil de usuario (y por ello, no se podrán hacer OneToOne), redirige a personas para que no se quede
    una la pantalla colgada y muestra el error existente. 
    """
    
    personas_disponibles = Persona.objects.filter(perfilusuario__isnull=True)
    if not personas_disponibles.exists():
        messages.error(request, "No hay personas disponibles. Primero debe crear una persona sin perfil de usuario.")
        return redirect("ver_personas")  # o la URL que prefiera
    
    datosFormulario = None
    if(request.method == 'POST'):
        datosFormulario = request.POST
    formulario = PerfilUsuarioModelForm(datosFormulario)
    
    if(request.method == "POST"):
        perfil_creado = crear_perfil_usuario_modelo(formulario)
        if(perfil_creado):
            messages.success(request, "Se ha creado el perfil de usuario "+formulario.cleaned_data.get('username')+ " correctamente")
            return redirect("ver_perfiles")
            
    return render(request, 'URLs/perfilesUsuario/create.html', {'formulario': formulario})


def crear_perfil_usuario_modelo(formulario):
    perfil_creado=False
    if formulario.is_valid():
        try:
            formulario.save()
            perfil_creado = True
        except Exception as error:
            print(error)
    
    return perfil_creado


## READ
def buscar_perfiles_usuarios(request):
    formulario = BusquedaPerfilesUsuariosForm(request.GET)
    
    if(len(request.GET) > 0):
        formulario = BusquedaPerfilesUsuariosForm(request.GET)
        
        if formulario.is_valid():
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"
            
            QSperfiles = PerfilUsuario.objects
            
            usernameBusqueda = formulario.cleaned_data.get('usernameBusqueda')
            rolesBusqueda = formulario.cleaned_data.get('rolBusqueda')
            esStaffBusqueda = formulario.cleaned_data.get('esStaffBusqueda')
            
            if(usernameBusqueda != ""):
                QSperfiles = QSperfiles.filter(username__contains=usernameBusqueda)
                mensaje_busqueda += "Username con contenido: "+usernameBusqueda + "\n"
            
            if len(rolesBusqueda )> 0:
                mensaje_busqueda += "Rol "+rolesBusqueda[0]
                queryOR = Q(rol = rolesBusqueda[0])
                
                for rol in rolesBusqueda[1:]:
                    mensaje_busqueda += " o " + rol
                    queryOR |= Q(rol = rol)
                mensaje_busqueda += "\n"
                QSperfiles = QSperfiles.filter(queryOR)
                
            if(esStaffBusqueda is not None):
                QSperfiles = QSperfiles.filter(es_staff=esStaffBusqueda)
                mensaje_busqueda += "Es staff: "+ ("si" if esStaffBusqueda else "no") + "\n"
            
            perfiles = QSperfiles.all()
            return render(request, 'URLs/perfilesUsuario/lista_perfiles.html', {
                'mostrar_perfiles': perfiles, 
                "texto_busqueda": mensaje_busqueda
            })

    else:
        formulario = BusquedaPerfilesUsuariosForm(None)
    
    return render(request, 'URLs/perfilesUsuario/busqueda_avanzada.html', {'formulario':formulario})


## UPDATE
def perfil_usuario_editar(request, perfil_id):
    perfil = PerfilUsuario.objects.get(id = perfil_id)
    datosFormulario = None
    
    if(request.method == 'POST'):
        datosFormulario = request.POST
    formulario = PerfilUsuarioUpdateForm(datosFormulario, instance = perfil)
    
    if(request.method == "POST"):
        if formulario.is_valid():
            try:
                formulario.save()
                messages.success(request, 'Se ha editado el perfil de usuario '+formulario.cleaned_data.get('username')+" correctamente")
                return redirect('ver_perfiles')
            except Exception as e:
                print(e)
    
    return render(request, 'URLs/perfilesUsuario/actualizar.html', {'formulario':formulario, 'perfil':perfil})



## DELETE
def perfil_usuario_eliminar(request, perfil_id):
    perfil = PerfilUsuario.objects.get(id = perfil_id)
    try:
        perfil.delete()
    except Exception as e:
        print(e)
    
    return redirect('ver_perfiles')
