from django.core.management.base import BaseCommand
from faker import Faker
from camping.models import *
from django.utils import timezone
from django.contrib.auth.hashers import make_password
import random

class Command(BaseCommand):
    help = 'Generando datos usando Faker'
    
    def handle(self, *args, **kwargs):
        fake = Faker('es_ES')

        recepcionistas = []
        cuidadores = []
        clientes = []

        # -----------------------------
        # 1. CREAR PERSONA + USUARIO
        # -----------------------------
        for _ in range(15):

            # Crear persona
            persona = Persona.objects.create(
                nombre=fake.first_name(),
                apellido=fake.last_name(),
                dni=fake.unique.nif(),
                fecha_nacimiento=fake.date_of_birth(minimum_age=18, maximum_age=90),
                telefono=fake.phone_number(),
            )

            # Crear usuario
            username = f"{persona.nombre.lower()}{random.randint(100,999)}"
            rol_usuario = random.choice([1, 2, 3, 4])
            password = make_password("12345678")

            usuario = Usuario.objects.create(
                username=username,
                password=password,
                email=fake.email(),
                rol=rol_usuario
            )

            # Asignar según rol
            if rol_usuario == Usuario.RECEPCIONISTA:
                recepcionistas.append((persona, usuario))
            elif rol_usuario == Usuario.CUIDADOR:
                cuidadores.append((persona, usuario))
            else:
                clientes.append((persona, usuario))

        # -----------------------------
        # 2. CREAR RECEPCIONISTAS
        # -----------------------------
        recep_objs = []
        for persona, usuario in recepcionistas:
            recep_objs.append(
                Recepcionista.objects.create(
                    usuario=usuario,
                    datos_persona=persona,
                    salario=round(random.uniform(1100, 2500), 2),
                    turno=random.choice(['ma', 'ta'])
                )
            )

        # -----------------------------
        # 3. CREAR CUIDADORES
        # -----------------------------
        cuida_objs = []
        for persona, usuario in cuidadores:
            cuida_objs.append(
                Cuidador.objects.create(
                    usuario=usuario,
                    datos_persona=persona,
                    especialidad=fake.job(),
                    disponible_de_noche=fake.boolean(),
                    puntuacion=random.randint(1, 10)
                )
            )

        # -----------------------------
        # 4. CREAR CLIENTES
        # -----------------------------
        cliente_objs = []
        for persona, usuario in clientes:
            cliente_objs.append(
                Cliente.objects.create(
                    usuario=usuario,
                    datos_persona=persona,
                    numero_cuenta=fake.iban(),
                    nacionalidad=fake.country(),
                    acepta_publicidad=fake.boolean()
                )
            )

        # -----------------------------
        # 5. CAMPINGS + PARCELAS
        # -----------------------------
        campings = []
        for _ in range(5):
            campings.append(
                Camping.objects.create(
                    nombre=fake.company(),
                    ubicacion=fake.address(),
                    estrellas=random.randint(1, 5),
                    sitio_web=fake.url()
                )
            )

        parcelas = []
        for camping in campings:
            usados = set()
            for _ in range(10):
                numero = fake.random_int(1, 100)
                while numero in usados:
                    numero = fake.random_int(1, 100)
                usados.add(numero)

                parcelas.append(
                    Parcela.objects.create(
                        camping=camping,
                        numero=numero,
                        capacidad=random.randint(2, 8),
                        tiene_sombra=fake.boolean()
                    )
                )

        # -----------------------------
        # 6. VEHÍCULOS
        # -----------------------------
        tipos = ['coche', 'moto', 'caravana']

        for cliente in cliente_objs:
            if fake.boolean(85):
                for _ in range(random.randint(1, 3)):
                    v = Vehiculo.objects.create(
                        tipo=random.choice(tipos),
                        matricula=fake.unique.license_plate(),
                        peso=round(random.uniform(500, 3500), 2),
                        marca=fake.company()
                    )
                    v.cliente.add(cliente)

        # -----------------------------
        # 7. ACTIVIDADES
        # -----------------------------
        actividades = [
            Actividad.objects.create(
                nombre=fake.word(),
                descripcion=fake.text(),
                cupo=random.randint(1, 30),
                precio=random.uniform(5, 50),
                requiere_material=fake.boolean()
            ) for _ in range(10)
        ]

        # -----------------------------
        # 8. RESERVAS
        # -----------------------------
        reservas = []
        for cliente in cliente_objs:
            for _ in range(random.randint(1, 3)):
                inicio = fake.date_this_year()
                fin = fake.date_between_dates(inicio, timezone.now().date())

                r = Reserva.objects.create(
                    cliente=cliente,
                    parcela=random.choice(parcelas),
                    fecha_inicio=inicio,
                    fecha_fin=fin
                )

                if fake.boolean(85):
                    r.actividades.set(random.sample(actividades, random.randint(1, 5)))

                reservas.append(r)

        # -----------------------------
        # 9. SERVICIOS EXTRA
        # -----------------------------
        servicios = [
            ServiciosExtra.objects.create(
                nombre=fake.word(),
                precio=random.uniform(5, 50),
                descripcion=fake.text(),
                disponible=fake.boolean()
            ) for _ in range(5)
        ]

        # -----------------------------
        # 10. RESERVAEXTRAS + FACTURAS
        # -----------------------------
        for reserva in reservas:
            re = ReservaExtras.objects.create(
                reserva_asociada=reserva,
                cantidad_solicitada=random.randint(1, 5),
                observaciones=fake.sentence()
            )
            re.servicios_extra.add(*random.sample(servicios, random.randint(1, 5)))

            Factura.objects.create(
                reserva_extra=re,
                total=round(random.uniform(50, 2000), 2),
                pagado=fake.boolean()
            )

        self.stdout.write(self.style.SUCCESS("Datos generados correctamente"))
