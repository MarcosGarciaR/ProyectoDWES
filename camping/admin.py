from django.contrib import admin

from .models import Persona, PerfilUsuario, Cliente, Recepcionista, Cuidador, Camping, Parcela, Vehiculo, Actividad, Reserva, ServiciosExtra, ReservaExtra, Factura

# Register your models here.
admin.site.register(Persona)
admin.site.register(PerfilUsuario)
admin.site.register(Recepcionista)
admin.site.register(Cuidador)
admin.site.register(Cliente)

admin.site.register(Camping)
admin.site.register(Parcela)
admin.site.register(Vehiculo)
admin.site.register(Actividad)

admin.site.register(Reserva)
admin.site.register(ServiciosExtra)
admin.site.register(ReservaExtra)

admin.site.register(Factura)


