from django.core.management.base import BaseCommand
from faker import Faker
from camping.models import *
import random

class Command(BaseCommand):
    help = 'Generando datos usando Faker'
    
    def handle(self, *args, **kwargs):
        fake = Faker('es_ES')
        
        personas = []
        for _ in range(15):
            p = Persona.objects.create(
                nombre = fake.first_name(),
                apellido = fake.last_name(),
                dni = fake.unique.nif(),
                fecha_nacimiento = fake.date_of_birth(minimum_age=1, maximum_age=100),
                email = fake.unique.email(),
                telefono = fake.phone_number()
            )
            personas.append(p)
            
            for persona in personas:
                perfil = PerfilUsuario.objects.create(
                    datos_usuario = persona,
                    username = fake.unique.user_name(),
                    password = fake.password(),
                    es_staff = fake.boolean(chance_of_getting_true=2),
                    fecha_registro = timezone.now()
                )
            
            for p in perfil[:1]:
                Recepcionista.objects.create(
                    usuario = p,
                    salario = round(random.uniform(1100, 2500), 2),
                    fecha_alta = fake.date_this_year(),
                    turno = random.choice(['ma','ta'])
                )
            
            for p in perfil[1:2]:
                Cuidador.objects.create(
                    usuario = p,
                    especialidad = fake.job(),
                    dispnible_de_noche = fake.boolean(),
                    puntuacion = random.randint(1, 10)
                )
            
            for p in 
            Cliente.objects.create(
                datos_cliente
                numero_cuenta
                nacionalidad
                acepta_publicidad
            )
            
            Camping.objects.create(
                nombre
                ubicacion
                estrellas
                sitio_web
            )
            
            Parcela.objects.create(
                camping
                numero
                capacidad
                tiene_sombra
            )
            
            Vehiculo.objects.create(
            tipo
            matricula
            peso
            cliente
            marca
            )
            
            Actividad.objects.create(
            nombre
            descripcion
            cupo
            precio
            requiere_material
            )
            
            Reserva.objects.create(
            cliente
            parcela
            fecha_inicio
            fecha_fin
            actividades
            
            )
            ServiciosExtra.objects.create(
            nombre
            precio
            descripcion
            disponible
            )
            
            ReservaExtra.objects.create(
            reserva
            servicios_extra
            cantidad_solicitada
            )
            
            Factura.objects.create(
            reserva
            total
            emitida_en
            pagado    
            )
            
        self.stdout.write(self.style.SUCCES('Datos generados correctamente'))