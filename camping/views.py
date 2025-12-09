from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.db.models import Avg, Max, Min, Q, Prefetch
from django.views.defaults import page_not_found
from django.contrib import messages

from datetime import datetime
from django.contrib.auth import login
from django.contrib.auth.decorators import permission_required

# Create your views here.

def index(request):
    if(not 'fecha_inicio' in request.session):
        request.session['fecha_inicio'] = datetime.now().strftime('%d/%m/%Y %H:%M')
    return render(request, 'index.html')

def borrar_session(request):
    del request.session['fecha_inicio']
    return render(request, 'index.html')


def registrar_usuario(request):
    if request.method == "POST":
        formulario = RegistroForm(request.POST)
        rol = request.POST.get('rol')
        persona = PersonaModelForm(request.POST)
        recepcionista = RegistroRecepcionistaForm(request.POST)
        cuidador = RegistroCuidadorForm(request.POST)
        cliente = RegistroClienteForm(request.POST)
            
        if formulario.is_valid() and persona.is_valid() and recepcionista.is_valid() and cuidador.is_valid() and cliente.is_valid():
            user = formulario.save()
            rol = int(formulario.cleaned_data.get('rol'))
            
            
            if(rol == Usuario.RECEPCIONISTA):
                salario = request.POST.get('salario')
                turno = request.POST.get('turno') 
                            
                recepcionista = Recepcionista.objects.create(usuario=user, salario=salario, turno=turno)
                recepcionista.save()
                messages.success(request, "Se ha creado el recepcionista correctamente")
            
            elif(rol == Usuario.CUIDADOR):
                especialidad = request.POST.get('especialidad')
                puntuacion = request.POST.get('puntuacion')
                cuidador = Cuidador.objects.create(usuario=user, especialidad=especialidad, puntuacion = puntuacion)
                cuidador.save()
                messages.success(request, "Se ha creado el cuidador correctamente")
            
            elif(rol == Usuario.CLIENTE):
                numero_cuenta = request.POST.get('numero_cuenta')
                nacionalidad = request.POST.get('nacionalidad')
                cliente = Cliente.objects.create(usuario=user, numero_cuenta=numero_cuenta, nacionalidad=nacionalidad)
                cliente.save()
                messages.success(request, "Se ha creado el cliente correctamente")
                
            login(request, user)
            return redirect('index')
    else:
        formulario = RegistroForm(None)
        persona = PersonaModelForm(None)
        recepcionista = RegistroRecepcionistaForm(None)
        cuidador = RegistroCuidadorForm(None)
        cliente = RegistroClienteForm(None)
        
    return render(request, 'registration/signup.html', {'formUsuario': formulario,  "formPersona": persona, "formRecepcionista": recepcionista, 
                                                        "formCuidador": cuidador, "formCliente": cliente}) 





"""
    if request.method == 'POST':
        usuario = RegistroForm(request.POST)
        persona = PersonaModelForm(request.POST)
        if usuario.is_valid() and persona.is_valid():
            user = usuario.save()
            persona = persona.save()
            
            rol = int(usuario.cleaned_data.get('rol'))
            
            if(rol == Usuario.RECEPCIONISTA):
                salario = usuario.cleaned_data.get('salario')
                turno = usuario.cleaned_data.get('turno') 
                            
                recepcionista = Recepcionista.objects.create(usuario=user, datos_persona = persona, salario=salario, turno=turno)
                recepcionista.save()
                
            elif(rol == Usuario.CUIDADOR):
                especialidad = usuario.cleaned_data.get('especialidad')
                puntuacion = usuario.cleaned_data.get('puntuacion')
                cuidador = Cuidador.objects.create(usuario=user, datos_persona = persona, especialidad=especialidad, puntuacion = puntuacion)
                cuidador.save()
                
            elif(rol == Usuario.CLIENTE):
                numero_cuenta = usuario.cleaned_data.get('numero_cuenta')
                nacionalidad = usuario.cleaned_data.get('nacionalidad')
                cliente = Cliente.objects.create(usuario=user, datos_persona = persona, numero_cuenta=numero_cuenta, nacionalidad=nacionalidad)
                cliente.save()
            
            login(request, user)
            return redirect('index')
    else:
        formulario = RegistroForm()
"""























#   Ordenar las reservas por fecha de inicio
def ver_reservas_por_fecha(request):
    reservas = Reserva.objects.select_related('cliente__datos_persona','parcela__camping').order_by('fecha_inicio').all()

    """
    reservas = (Reserva.objects.raw("SELECT cr.id AS id, cp.nombre, cp.apellido, cr.fecha_inicio, cr.fecha_fin  FROM camping_reserva cr "
                                    + " JOIN camping_cliente cc ON cr.cliente_id = cc.id "
                                    + " JOIN camping_persona cp ON cc.id = cp.id "
                                    "   ORDER BY cr.fecha_inicio"))
    """
    
    return render(request, 'URLs/reservas/reservas_fecha.html', {"mostrar_reservas":reservas})


#   Ver la reserva cuyo ID se pasa por la URL
def ver_reserva_por_id(request, id_reserva):
    reserva = Reserva.objects.select_related('cliente__datos_persona').prefetch_related("actividades").get(id=id_reserva)
    
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
    
    return render(request, 'URLs/facturas/lista_facturas.html',{'mostrar_facturas':facturas})


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
    cuidadores = Cuidador.objects.select_related('datos_persona').filter(Q(puntuacion__gt=puntuacionPedida) | Q(disponible_de_noche=True)).all()
    
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
    clientes = Cliente.objects.select_related('datos_persona').filter(vehiculos=None).all()
    
    """
    clientes = Cliente.objects.raw("SELECT * FROM camping_cliente cc"
                                    + "WHERE cc.id NOT IN ("SELECT cliente_id FROM camping_vehiculo_cliente")")
    """
    
    return render(request, 'URLs/clientes/clientes_sin_vehiculo.html', {'mostrar_clientes_sin_vehiculo':clientes})


#   Mostrar las reservas que no tienen actividades asociadas
def reservas_sin_actividades(request):
    reservas = Reserva.objects.select_related("cliente__datos_persona").prefetch_related(Prefetch("actividades")).filter(actividades=None).order_by('id')[:10].all()
    
    """
    reservas = Reserva.objects.raw("SELECT * FROM camping_reserva cr"
                                    + "WHERE cr.id NOT IN ("SELECT reserva_id FROM camping_reserva_actividades")")
    """
    
    return render(request, 'URLs/reservas/reservas_sin_actividades.html', {'mostrar_reservas':reservas})


#   Ver las reservas que ha realizado un cliente.
def reservas_de_cliente_por_id(request, cliente_id):
    cliente = Cliente.objects.select_related('datos_persona') .prefetch_related("reservas").get(id=cliente_id)
    
    """
    cliente = Cliente.objects.raw("SELECT * FROM camping_cliente cc"
                                    + "JOIN camping_datos_persona cdc ON c.datos_persona_id = cdc.id"
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




"""=================================================================================FORMULARIOS========================================================================================================================="""
#   Ver la lista de personas
def ver_personas(request):
    personas = Persona.objects.all()
    
    """
    personas = (Persona.objects.raw(" SELECT * FROM camping_persona p"))
    """
    
    return render(request, 'URLs/personas/lista_personas.html', {"mostrar_personas":personas})

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
                mensaje_busqueda += f"Nombre con contenido: {nombreBusqueda}" + "\n"
            
            if(apellidosBusqueda != ""):
                QSpersonas = QSpersonas.filter(apellido__contains=apellidosBusqueda)
                mensaje_busqueda += f"Apellido con contenido: {apellidosBusqueda}" + "\n"
            
            if(dni != ""):
                QSpersonas = QSpersonas.filter(dni__contains=dni)
                mensaje_busqueda += "Con DNI: {dni}"+ "\n"
            
            if(annio_nacimiento != None ):
                QSpersonas = QSpersonas.filter(fecha_nacimiento__year= annio_nacimiento)
                mensaje_busqueda += f"Con año de nacimiento: {annio_nacimiento}"
            
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

"""=================================================================================RECEPCIONISTAS========================================================================================================================="""
def ver_recepcionistas(request):
    recepcionistas = Recepcionista.objects.all()
    """
    recepcionistas = Recepcionista.objects.raw(" SELECT * FROM camping_recepcionista cr "
                                                + "JOIN camping_perfilusuario cpu ON cr.usuario_id = cpu.id ")
    """
    return render(request, 'URLs/recepcionistas/recepcionistas.html', {'recepcionistas':recepcionistas})


## CREATE
def crear_recepcionista(request):
    datosFormulario = None
    if(request.method == 'POST'):
        datosFormulario = request.POST
    
    formulario = RecepcionistaModelForm(datosFormulario)
    if(request.method == "POST"):
        recepcionista_creado = crear_recepcionista_modelo(formulario)
        if(recepcionista_creado):
            messages.success(request, "Se ha creado al recepcionista con salario "+str(formulario.cleaned_data.get('salario'))+ " correctamente")
            return redirect("ver_recepcionistas")
        
    return render(request, 'URLs/recepcionistas/create.html', {'formulario':formulario})
    
def crear_recepcionista_modelo(formulario):
    recepcionista_creado=False
    if formulario.is_valid():
        try:
            formulario.save()
            recepcionista_creado = True
        except Exception as error:
            print(error)
    return recepcionista_creado


## READ
def buscar_recepcionistas(request):
    formulario = BusquedaRecepcionistasForm(request.GET)

    if len(request.GET) > 0:
        formulario = BusquedaRecepcionistasForm(request.GET)

        if formulario.is_valid():
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"

            QSrecepcionistas = Recepcionista.objects

            salario = formulario.cleaned_data.get('salario')
            fecha_desde = formulario.cleaned_data.get('fecha_desde')
            fecha_hasta = formulario.cleaned_data.get('fecha_hasta')
            turno = formulario.cleaned_data.get('turno') 


            if salario is not None:
                QSrecepcionistas = QSrecepcionistas.filter(salario__gte=salario)
                mensaje_busqueda += f"Salario mayor o igual a: {salario} \n"


            if fecha_desde is not None:
                QSrecepcionistas = QSrecepcionistas.filter(fecha_alta__gte=fecha_desde)
                mensaje_busqueda += f"Fecha de alta desde: {fecha_desde} \n"


            if fecha_hasta is not None:
                QSrecepcionistas = QSrecepcionistas.filter(fecha_alta__lte=fecha_hasta)
                mensaje_busqueda += f"Fecha de alta hasta: {fecha_hasta} \n"
            
            if len(turno )> 0:
                mensaje_busqueda += "Turno "+turno[0]
                queryOR = Q(turno = turno[0])
                
                for turno in turno[1:]:
                    mensaje_busqueda += " o " + turno
                    queryOR |= Q(turno = turno)
                mensaje_busqueda += "\n"
                QSrecepcionistas = QSrecepcionistas.filter(queryOR)
                
            recepcionistas = QSrecepcionistas.all()

            return render(request,'URLs/recepcionistas/recepcionistas.html',{'recepcionistas': recepcionistas,'texto_busqueda': mensaje_busqueda})

    else:
        formulario = BusquedaRecepcionistasForm(None)

    return render(
        request,
        'URLs/recepcionistas/busqueda_avanzada.html',
        {'formulario': formulario}
    )


## UPDATE
def recepcionista_editar(request, recepcionista_id):
    recepcionista = Recepcionista.objects.get(id = recepcionista_id)
    datosFormulario = None

    if(request.method == "POST"):
        datosFormulario = request.POST
    formulario = RecepcionistaModelForm(datosFormulario, instance = recepcionista)

    if(request.method == "POST"):
        if formulario.is_valid():
            try:
                formulario.save()
                messages.success(request, 'Se ha editado al recepcionista con salario '+formulario.cleaned_data.get('salario')+" correctamente")
                return redirect('ver_recepcionistas')
            except Exception as e:
                print(e)
    
    return render(request, 'URLs/recepcionistas/actualizar.html', {'formulario':formulario, 'recepcionista':recepcionista})


## DELETE
def recepcionista_eliminar(request, recepcionista_id):
    recepcionista = Recepcionista.objects.get(id = recepcionista_id)
    try:
        recepcionista.delete()
    except Exception as e:
        print(e)
    return redirect('ver_recepcionistas')




"""=================================================================================CAMPINGS========================================================================================================================="""
#   Ver la lista de campings
def ver_campings(request):
    campings = Camping.objects.all()
    
    """
    campings = (Camping.objects.raw(" SELECT * FROM camping_camping c"))
    """
    
    return render(request, 'URLs/campings/lista_campings.html', {"mostrar_campings":campings})


## CREATE
def crear_camping(request):
    datosFormulario = None
    if(request.method == 'POST'):
        datosFormulario = request.POST
    
    formulario = CampingModelForm(datosFormulario)
    if(request.method == "POST"):
        camping_creado = crear_camping_modelo(formulario)
        if(camping_creado):
            messages.success(request, "Se ha creado al camping con nombre " + formulario.cleaned_data.get('nombre') + " correctamente")
            return redirect("ver_campings")
        
    return render(request, 'URLs/campings/create.html', {'formulario':formulario})
    
def crear_camping_modelo(formulario):
    camping_creado=False
    if formulario.is_valid():
        try:
            formulario.save()
            camping_creado = True
        except Exception as error:
            print(error)
    return camping_creado


def buscar_campings(request):
    formulario = BusquedaCampingsForm(request.GET)
    
    if(len(request.GET) > 0):
        formulario = BusquedaCampingsForm(request.GET)
        
        if formulario.is_valid():
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"
            
            # QUERY SETS AQUI
            QScampings = Camping.objects
            
            nombre = formulario.cleaned_data.get('nombre')
            ubicacion = formulario.cleaned_data.get('ubicacion')
            estrellas = formulario.cleaned_data.get('estrellas')
            sitio_web = formulario.cleaned_data.get('sitio_web')            
            
            
            if(nombre != ""):
                QScampings = QScampings.filter(nombre__contains=nombre)
                mensaje_busqueda += "Su nombre contenga "+nombre
                
            if(ubicacion != ""):
                QScampings = QScampings.filter(ubicacion__contains=ubicacion)
                mensaje_busqueda += "Su ubicación contenga "+ubicacion
                
            if( estrellas != None):
                QScampings = QScampings.filter(estrellas__gte=estrellas)
                mensaje_busqueda += "Con una puntuación igual o superior a "+ str(estrellas) + " estrellas"
            
            if(sitio_web != ""):
                QScampings = QScampings.filter(sitio_web__contains=sitio_web)
                mensaje_busqueda += "El nombre de su sitio web contenga "+sitio_web
            
            campings = QScampings.all()
            return render(request, 'URLs/campings/lista_campings.html', {'mostrar_campings':campings, "texto_busqueda":mensaje_busqueda})

    else:
        formulario = BusquedaCampingsForm(None)
    
    return render(request, 'URLs/campings/busqueda_avanzada.html', {'formulario':formulario})

## UPDATE
def camping_editar(request, camping_id):
    camping = Camping.objects.get(id = camping_id)
    datosFormulario = None

    if(request.method == "POST"):
        datosFormulario = request.POST
    formulario = CampingModelForm(datosFormulario, instance = camping)

    if(request.method == "POST"):
        if formulario.is_valid():
            try:
                formulario.save()
                messages.success(request, 'Se ha editado el camping con nombre '+formulario.cleaned_data.get('nombre')+" correctamente")
                return redirect('ver_campings')
            except Exception as e:
                print(e)
    
    return render(request, 'URLs/campings/actualizar.html', {'formulario':formulario, 'camping':camping})

## DELETE
def camping_eliminar(request, camping_id):
    camping = Camping.objects.get(id = camping_id)
    try:
        camping.delete()
    except Exception as e:
        print(e)
    return redirect('ver_campings')


"""=================================================================================PARCELAS========================================================================================================================="""

def ver_parcelas(request):
    parcelas = Parcela.objects.select_related('camping').all().order_by('camping__nombre', 'numero')
    
    return render(request, 'URLs/parcelas/lista_parcelas.html', {'mostrar_parcelas':parcelas})

## CREATE
def crear_parcela(request):
    datosFormulario = None
    if(request.method == 'POST'):
        datosFormulario = request.POST
    
    formulario = ParcelaModelForm(datosFormulario)
    if(request.method == "POST"):
        parcela_creado = crear_parcela_modelo(formulario)
        if(parcela_creado):
            messages.success(request,  f"Se ha creado la parcela con número {formulario.cleaned_data.get('numero')} correctamente")
            return redirect("ver_parcelas")
        
    return render(request, 'URLs/parcelas/create.html', {'formulario':formulario})
    
def crear_parcela_modelo(formulario):
    parcela_creado=False
    if formulario.is_valid():
        try:
            formulario.save()
            parcela_creado = True
        except Exception as error:
            print(error)
    return parcela_creado


def buscar_parcelas(request):
    formulario = BusquedaParcelasForm(request.GET)
    
    if(len(request.GET) > 0):
        formulario = BusquedaParcelasForm(request.GET)
        
        if formulario.is_valid():
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"
            
            QSparcelas = Parcela.objects
            
            numero = formulario.cleaned_data.get('numero')
            capacidad = formulario.cleaned_data.get('capacidad')
            tiene_sombra = formulario.cleaned_data.get('tiene_sombra')
            nombre_camping = formulario.cleaned_data.get('nombre_camping')
                        
            
            if(numero is not None):
                QSparcelas  = QSparcelas .filter(numero = numero)
                mensaje_busqueda += f"Numero de parcela: {numero}"
                
            if(capacidad is not None ):
                QSparcelas  = QSparcelas .filter(capacidad__lte=capacidad)
                mensaje_busqueda += f"Capacidad máxima: {capacidad}"
                
            if( tiene_sombra is not None):
                QSparcelas  = QSparcelas .filter(tiene_sombra=tiene_sombra)
                mensaje_busqueda += f"Con sombra: {tiene_sombra}"
            
            if(nombre_camping  != ""):
                QSparcelas = QSparcelas.filter(camping__nombre__icontains=nombre_camping)
                mensaje_busqueda += f"El nombre del camping contenga {nombre_camping}"
            
            parcelas = QSparcelas .all()
            return render(request, 'URLs/parcelas/lista_parcelas.html', {'mostrar_parcelas':parcelas, "texto_busqueda":mensaje_busqueda})

    else:
        formulario = BusquedaParcelasForm(None)
    
    return render(request, 'URLs/parcelas/busqueda_avanzada.html', {'formulario':formulario})

## UPDATE
def parcela_editar(request, parcela_id):
    parcela = Parcela.objects.get(id = parcela_id)
    datosFormulario = None

    if(request.method == "POST"):
        datosFormulario = request.POST
    formulario = ParcelaModelForm(datosFormulario, instance = parcela)

    if(request.method == "POST"):
        if formulario.is_valid():
            try:
                formulario.save()
                messages.success(request, f"Se ha editado la parcela con numero {formulario.cleaned_data.get('numero')} correctamente")
                return redirect('ver_parcelas')
            except Exception as e:
                print(e)
    
    return render(request, 'URLs/parcelas/actualizar.html', {'formulario':formulario, 'parcela':parcela})

## DELETE
def parcela_eliminar(request, parcela_id):
    parcela = Parcela.objects.get(id = parcela_id)
    try:
        parcela.delete()
    except Exception as e:
        print(e)
    return redirect('ver_parcelas')


"""=================================================================================FACTURAS========================================================================================================================="""

def ver_facturas(request):
    facturas = Factura.objects.all()
    
    """
    campings = (Camping.objects.raw(" SELECT * FROM camping_camping c"))
    """
    
    return render(request, 'URLs/facturas/lista_facturas.html', {"mostrar_facturas":facturas})


## CREATE
def crear_factura(request):
    datosFormulario = None
    if(request.method == 'POST'):
        datosFormulario = request.POST
    
    formulario = FacturaModelForm(datosFormulario)
    if(request.method == "POST"):
        factura_creado = crear_factura_modelo(formulario)
        if(factura_creado):
            messages.success(request, f"Se ha creado la factura con fecha de emisión: {formulario.cleaned_data.get('emitida_en')} correctamente")
            return redirect("ver_facturas")
        
    return render(request, 'URLs/facturas/create.html', {'formulario':formulario})
    
def crear_factura_modelo(formulario):
    factura_creado=False
    if formulario.is_valid():
        try:
            formulario.save()
            factura_creado = True
        except Exception as error:
            print(error)
    return factura_creado


def buscar_facturas(request):
    formulario = BusquedaFacturasForm(request.GET)
    
    if(len(request.GET) > 0):
        formulario = BusquedaFacturasForm(request.GET)
        
        if formulario.is_valid():
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"
            
            # QUERY SETS AQUI
            QSfacturas = Factura.objects
            
            reserva_extra = formulario.cleaned_data.get('reserva_extra')
            pagado = formulario.cleaned_data.get('pagado')
            fecha_inicio = formulario.cleaned_data.get('fecha_inicio')
            fecha_fin = formulario.cleaned_data.get('fecha_fin')
            
            if(reserva_extra is not None):
                QSfacturas = QSfacturas.filter(reserva_extra__id = reserva_extra)
                mensaje_busqueda += f"ID de reserva {reserva_extra}"
            
            if (pagado is not None):
                QSfacturas = QSfacturas.filter(pagado = pagado)
                mensaje_busqueda += f"Estado del pago: {'Pagado' if pagado else 'A la espera'}"
            
            if fecha_inicio:
                QSfacturas = QSfacturas.filter(emitida_en__date__gte=fecha_inicio)
                mensaje_busqueda += f"Emitida desde: {fecha_inicio}"

            if fecha_fin:
                QSfacturas = QSfacturas.filter(emitida_en__date__lte=fecha_fin)
                mensaje_busqueda += f"Emitida hasta: {fecha_fin}"
            
            facturas = QSfacturas.all()
            return render(request, 'URLs/facturas/lista_facturas.html', {'mostrar_facturas':facturas, "texto_busqueda":mensaje_busqueda})

    else:
        formulario = BusquedaFacturasForm(None)
    
    return render(request, 'URLs/facturas/busqueda_avanzada.html', {'formulario':formulario})

## UPDATE
def factura_editar(request, factura_id):
    factura = Factura.objects.get(id = factura_id)
    datosFormulario = None

    if(request.method == "POST"):
        datosFormulario = request.POST
    formulario = FacturaModelForm(datosFormulario, instance = factura)

    if(request.method == "POST"):
        if formulario.is_valid():
            try:
                formulario.save()
                messages.success(request, f"Se ha editado la factura con fecha de emisión: {formulario.cleaned_data.get('emitida_en')} correctamente")
                return redirect('ver_facturas')
            except Exception as e:
                print(e)
    
    return render(request, 'URLs/facturas/actualizar.html', {'formulario':formulario, 'factura':factura})

## DELETE
def factura_eliminar(request, factura_id):
    factura = Factura.objects.get(id = factura_id)
    try:
        factura.delete()
    except Exception as e:
        print(e)
    return redirect('ver_facturas')

