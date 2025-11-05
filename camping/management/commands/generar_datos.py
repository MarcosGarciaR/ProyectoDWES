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
        
        recepcionistas = []
        cuidadores = []
        no_staff = []
        OPCIONES_STAFF = ['recepcionista','cuidador','cliente']
        for persona in personas:
            perfil = PerfilUsuario.objects.create(
                datos_usuario = persona,
                username = fake.unique.user_name(),
                password = fake.password(),
                es_staff = fake.boolean(chance_of_getting_true=20),
                fecha_registro = timezone.now()
            )
            
            if(perfil.es_staff):
                rol = random.choice(OPCIONES_STAFF)
                if(rol == 'recepcionista'):
                    recepcionistas.append(perfil)
                else:
                    cuidadores.append(perfil)
            else:
                rol = 'cliente'
                no_staff.append(perfil)
        
        for r in recepcionistas:
            Recepcionista.objects.create(
                usuario = r,
                salario = round(random.uniform(1100, 2500), 2),
                fecha_alta = fake.date_this_year(),
                turno = random.choice(['ma','ta'])
            )
        
        for c in cuidadores:
            Cuidador.objects.create(
                usuario = c,
                especialidad = fake.job(),
                disponible_de_noche = fake.boolean(),
                puntuacion = random.randint(1, 10)
            )
        
        clientes = []
        for p in no_staff:
            cliente = Cliente.objects.create(
            datos_cliente = p.datos_usuario,
            numero_cuenta = fake.iban(),
            nacionalidad = fake.current_country(),
            acepta_publicidad = fake.boolean()
        )
            clientes.append(cliente)
        
        campings = []
        for _ in range(5):
            c = Camping.objects.create(
                nombre = fake.company(),
                ubicacion = fake.address(),
                estrellas = random.randint(1, 5),
                sitio_web = fake.url()
            )
            campings.append(c)
            
        parcelas = []
        for c in campings:
            numeros_usados = set()
            for _ in range(10):
                numero_actual = fake.random_int(min=1, max=100)
                while(numero_actual in numeros_usados):
                    numero_actual = fake.random_int(min=1, max=100)
                
                
                parcelas.append(Parcela.objects.create(
                camping = c,
                numero = numero_actual,
                capacidad = random.randint(2,8),
                tiene_sombra = fake.boolean()
                )
            )
        
        OPCIONES_VEHICULO = ['coche','moto','caravana']
        for cl in clientes:
            if fake.boolean(chance_of_getting_true=85):
                for _ in range(random.randint(1, 3)):
                    v = Vehiculo.objects.create(
                        tipo = fake.random.choice(OPCIONES_VEHICULO),
                        matricula = fake.unique.license_plate(),
                        peso = round(random.uniform(500, 3500), 2),
                        marca = fake.company()
                    )
                v.cliente.add(cl)
            
        actividades = []
        for _ in range(10):
            actividades.append(Actividad.objects.create(
            nombre = fake.word(),
            descripcion = fake.text(),
            cupo = fake.random_int(1, 30),
            precio = random.uniform(5,50),
            requiere_material = fake.boolean()
        ))
        
        reservas = []    
        for c in clientes:
            for _ in range(random.randint(1,3)):
                miFecha_inicio = fake.date_this_year()
                r = Reserva.objects.create(
                    cliente = c,
                    parcela = random.choice(parcelas),
                fecha_inicio = miFecha_inicio, 
                fecha_fin =  fake.date_between_dates(miFecha_inicio, date_end=timezone.now().date()),
                
                )
                if fake.boolean(chance_of_getting_true=85):
                    r.actividades.set(random.sample(actividades, random.randint(1,5)))
                reservas.append(r)
        
        servicios = []
        for _ in range(5):
            servicios.append(ServiciosExtra.objects.create(
            nombre = fake.word(),
            precio = random.uniform(5, 50),
            descripcion = fake.text(),
            disponible =  fake.boolean()
        ))
        
        for r in reservas:
            re = ReservaExtras.objects.create(
            reserva_asociada = r,
            cantidad_solicitada = fake.random_int(1, 5),
            observaciones = fake.sentence(),
            )
            re.servicios_extra.add(*random.sample(servicios, random.randint(1, 5)))
            
            Factura.objects.create(
                reserva_extra = re,
                total = round(random.uniform(50, 2000), 2),
                emitida_en = timezone.now(), 
                pagado = fake.boolean()
            )
        
        self.stdout.write(self.style.SUCCESS('Datos generados correctamente'))