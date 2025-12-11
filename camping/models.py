from django.db import models
from django.utils import timezone

from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser 


# Create your models here.
# USUARIO
class Usuario(AbstractUser):
    ADMINISTRADOR = 1
    RECEPCIONISTA = 2  
    CUIDADOR = 3
    CLIENTE = 4
    ROLES = (
        (ADMINISTRADOR , 'administrador'),
    (RECEPCIONISTA, 'recepcionista'),
    (CUIDADOR , 'cuidador'),
    (CLIENTE , 'cliente'),
    )

    rol = models.PositiveSmallIntegerField(
        choices = ROLES, default=1
    )
    
# PERSONA
class Persona(models.Model):
    
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=20, default="")
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.dni}"    
    
# RECEPCIONISTA
class Recepcionista(models.Model):
    OPCIONES_TURNO = [
        ('ma', 'Mañana'),
        ('ta', 'Tarde')
    ]
    usuario = models.OneToOneField(Usuario, on_delete= models.CASCADE, null=True)
    
    datos_persona = models.OneToOneField(Persona, on_delete=models.CASCADE)
    salario = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    turno = models.CharField(max_length=20, choices=OPCIONES_TURNO, blank=True, null=True)
    
# CUIDADOR
class Cuidador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete= models.CASCADE, null=True)
    
    datos_persona = models.OneToOneField(Persona, on_delete=models.CASCADE, blank=True, null=True)
    especialidad = models.CharField(max_length=50, blank=True, null=True)
    disponible_de_noche = models.BooleanField(default=False, blank=True, null=True)
    puntuacion = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], default=5)

# CLIENTE
class Cliente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete= models.CASCADE, null=True)
    
    datos_persona = models.OneToOneField(Persona, on_delete=models.CASCADE, default="")
    numero_cuenta = models.CharField(max_length=30, blank=True, null=True)
    nacionalidad = models.CharField(max_length=50, blank=True, null=True)
    acepta_publicidad = models.BooleanField(default=False, blank=True, null=True)




# CAMPING
class Camping(models.Model):
    nombre = models.CharField(max_length=150)
    ubicacion = models.CharField(max_length=200)
    estrellas = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    sitio_web = models.URLField(null=True, blank=True)
    
    def __str__(self):
        return self.nombre

# PARCELA
class Parcela(models.Model):
    camping = models.ForeignKey(Camping, on_delete=models.CASCADE)
    numero = models.IntegerField(unique=False)
    capacidad = models.PositiveIntegerField(default=2, validators=[MinValueValidator(1), MaxValueValidator(25)])
    tiene_sombra = models.BooleanField(default=False)
    
    def __str__(self):
            return f"Parcela {self.numero} - {self.camping.nombre}"
        
# VEHÍCULO
class Vehiculo(models.Model):
    OPCIONES_VEHICULO = [
        ('coche', 'Coche'),
        ('moto', 'Moto'),
        ('caravana', 'Caravana')
    ]
    
    tipo = models.CharField(max_length=50, choices=OPCIONES_VEHICULO)
    matricula = models.CharField(max_length=20, unique=True)
    peso = models.FloatField(help_text="Introduce el peso aproximado en Kilogramos", null=False)
    cliente = models.ManyToManyField(Cliente, related_name="vehiculos")
    marca = models.CharField(max_length=25, null=True)
    
# ACTIVIDAD
class Actividad(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    cupo = models.PositiveIntegerField()
    precio = models.FloatField()
    requiere_material = models.BooleanField(default=False)


# RESERVA
class Reserva(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="reservas")
    parcela = models.ForeignKey(Parcela, on_delete=models.PROTECT)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    actividades = models.ManyToManyField(Actividad, related_name="actividades")

# ServiciosEXTRA
class ServiciosExtra(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=6, decimal_places=2) 
    descripcion = models.TextField(blank=True)
    disponible = models.BooleanField(default=True)

# RESERVAEXTRAS
class ReservaExtras(models.Model):
    reserva_asociada = models.OneToOneField(Reserva, on_delete=models.CASCADE)
    servicios_extra = models.ManyToManyField(ServiciosExtra)
    cantidad_solicitada = models.IntegerField(default=1)
    observaciones = models.CharField(max_length=150, null=True, blank=True)


# FACTURA
class Factura(models.Model):
    reserva_extra = models.OneToOneField(ReservaExtras, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    emitida_en = models.DateTimeField(default=timezone.now)
    pagado = models.BooleanField(default=False)