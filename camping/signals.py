from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone
import secrets




@receiver(user_logged_in)
def set_session_variables(sender, request, user, **kwargs):
    # Variables de la sesión
    request.session['user_role'] = user.get_rol_display()
    request.session['login_time'] = timezone.localtime(timezone.now()).strftime('%d/%m/%Y %H:%M:%S')
    request.session['user_email'] = user.email
    request.session['session_id_custom'] = secrets.token_hex(4) 


"""
Para los permisos, he visto que se puede crear manualmente y prefiero dejarlo por si acaso, aún así en este caso los voy a crear manualmente en la pantalla del admin (para mi es menos lioso).

from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps

@receiver(post_migrate)
def crear_grupos_y_permisos(sender, **kwargs):
    if sender.name == "camping":  
        # Crear grupos si no existen (En mi caso ya los había creado, pero lo dejo por si me sirve de apuntes a futuro)
        recepcionistas, _ = Group.objects.get_or_create(name="Recepcionistas")
        cuidadores, _ = Group.objects.get_or_create(name="Cuidadores")
        clientes, _ = Group.objects.get_or_create(name="Clientes")

        # Asignar permisos a cada grupo
        Recepcionista = apps.get_model("camping", "Recepcionista")
        Cuidador = apps.get_model("camping", "Cuidador")
        Cliente = apps.get_model("camping", "Cliente")
        Reserva = apps.get_model("camping", "Reserva")
        Vehiculo = apps.get_model("camping", "Vehiculo")
        Factura = apps.get_model("camping", "Factura")
        Actividad = apps.get_model("camping", "Actividad")
        Camping = apps.get_model("camping", "Camping")
        Parcela = apps.get_model("camping", "Parcela")
        ServiciosExtra = apps.get_model("camping", "ServiciosExtra")
        ReservaExtra = apps.get_model("camping", "ReservaExtra")

        perms_recepcionista = Permission.objects.filter(content_type__app_label="camping", content_type__model="recepcionista")
        perms_cuidador = Permission.objects.filter(content_type__app_label="camping", content_type__model="cuidador")
        perms_cliente = Permission.objects.filter(content_type__app_label="camping", content_type__model="cliente")

        recepcionistas.permissions.set(perms_recepcionista)
        cuidadores.permissions.set(perms_cuidador)
        clientes.permissions.set(perms_cliente)
        
        
        # ---------------- Recepcionista ----------------
        perms_recepcionista = Permission.objects.filter(content_type__app_label="camping",).filter(# Todos los permisos de estos modelos
            content_type__model__in=["camping", "parcela", "vehiculo", "factura", "serviciosextra", "reservaextra"]) | Permission.objects.filter(content_type__app_label="camping",content_type__model="reserva",codename__in=["view_reserva", "change_reserva", "delete_reserva"])
        recepcionistas.permissions.set(perms_recepcionista)

        # ---------------- Cuidador ----------------
        perms_cuidador = Permission.objects.filter(content_type__app_label="camping",content_type__model="actividad") | Permission.objects.filter(content_type__app_label="camping",content_type__model__in=["reserva", "vehiculo", "camping", "parcela", "serviciosextra", "reservaextra"],codename__startswith="view")
        cuidadores.permissions.set(perms_cuidador)

        # ---------------- Cliente ----------------
        perms_cliente = Permission.objects.filter(content_type__app_label="camping",content_type__model="reserva",codename__in=["add_reserva", "view_reserva"]) | Permission.objects.filter(content_type__app_label="camping",content_type__model="vehiculo",codename__in=["add_vehiculo", "view_vehiculo", "delete_vehiculo"]) | Permission.objects.filter(content_type__app_label="camping",content_type__model__in=["actividad", "camping", "parcela", "serviciosextra", "reservaextra", "factura"],codename__startswith="view")
        clientes.permissions.set(perms_cliente)
"""