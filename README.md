# ProyectoDWES
Este proyecto tratará sobre una página web dedicada en un sistema de gestión de campings.
Esta web permitirá administrar clientes, empleados, reservas, actividades y facturación.

## DEFINICIÓN DE LOS MODELOS
### **Persona** 
Descripción: 
Modelo base que contiene los atributos comunes para todos los usuarios del sistema (clientes, recepcionistas, cuidadores).

Atributos:
- `nombre` (CharField, max_length=100): Nombre de la persona.
- `apellido` (CharField, max_length=100): Apellido de la persona.
- `dni` (CharField, max_length=20, unique=True): Documento Nacional de Identidad, identificador único.
- `fecha_nacimiento` (DateField): Fecha de nacimiento.
- `email` (EmailField, unique=True, default=""): Correo electrónico, único en la base de datos. Se utiliza el atributo EmailField que sirve para el control de estos.
- `telefono` (CharField, max_length=20, default=""): Número de teléfono.

### **PerfilUsuario**
Descripción: 
Perfil de usuario asociado a una persona para control de autenticación y permisos.

Atributos:
- `datos_usuario` (OneToOneField a Persona, on_delete=models.CASCADE): Relación uno a uno con Persona.
- `username` (CharField, max_length=50, unique=True, default=""): Nombre de usuario único.
- `password` (CharField, max_length=128): Contraseña cifrada del usuario. Por ahora no tiene ningún control de carácteres.
- `es_staff` (BooleanField, default=False): Indica si el usuario pertenece a la administración. Para futuros permisos a trabajadores.
- `fecha_registro` (DateTimeField, default=timezone.now): Fecha y hora de registro.

### **Recepcionista**
Descripción: 
Empleado de recepción en el camping.

Atributos:
- `usuario` (OneToOneField a PerfilUsuario, on_delete=models.CASCADE): Usuario asignado al recepcionista.
- `salario` (DecimalField, max_digits=8, decimal_places=2): Salario mensual. Con algunos controles lógicos.
- `fecha_alta` (DateField): Fecha en la que fue contratado.
- `turno` (CharField, choices=OPCIONES_TURNO, max_length=20): Turno asignado (a elegir entre mañana o tarde).

### **Cuidador**
Descripción: 
Empleado encargado del cuidado de usuarios e instalaciones.

Atributos:
- `usuario` (OneToOneField a PerfilUsuario, on_delete=models.CASCADE): Usuario de la web asignado al cuidador.
- `especialidad` (CharField, max_length=50): Área de especialización. 
- `disponible_de_noche` (BooleanField, default=False): Indica si está disponible por la noche.
- `puntuacion` (IntegerField, validators=[MinValueValidator(1), MaxValueValidator(10)]): Valoración del cuidador de 1 a 10.

### **Cliente**
Descripción: 
Persona que utiliza los servicios del camping.

Atributos:
- `datos_cliente` (OneToOneField a Persona, on_delete=models.CASCADE): Datos personales asociados.
- `numero_cuenta` (CharField, max_length=30, blank=True, null=True): Cuenta bancaria del cliente, puede estar en blanco (Una reserva de 5 personas, a nombre de un único cliente).
- `nacionalidad` (CharField, max_length=50): Nacionalidad del cliente.
- `acepta_publicidad` (BooleanField, default=False): Permiso para recibir publicidad.

### **Camping**
Descripción: 
Información general del camping.

Atributos:
- `nombre` (CharField, max_length=150): Nombre del camping.
- `ubicacion` (CharField, max_length=200): Dirección.
- `estrellas` (IntegerField, validators=[MinValueValidator(1), MaxValueValidator(5)]): Clasificación por estrellas (1 a 5). Parámetro validators que permite únicamente los valores indicados.
- `sitio_web` (URLField, null=True, blank=True): Página web oficial, opcional. Se utiliza el atributo URLField que permite agregar URLs (Aunque todos los campings se gestionen de manera "centralizada", cada uno de ellos debería tener su propia dirección web, o dentro de la misma, distintas rutas).

### **Parcela**
Descripción: 
Parcelas dentro del camping disponibles para reservar.

Atributos:
- `camping` (ForeignKey a Camping, on_delete=models.CASCADE): Camping en el que se encuentra la parcela.
- `numero` (IntegerField, unique=True): Número identificador único de la parcela.
- `capacidad` (PositiveIntegerField, default=2): Capacidad máxima de personas, por defecto para 2 personas.
- `tiene_sombra` (BooleanField, default=False): Indica si la parcela tiene sombra (Para plus de precio).

### **Vehiculo**
Descripción: 
Vehículos registrados por los clientes.

Atributos:
- `tipo` (CharField, choices=OPCIONES_VEHICULO, max_length=50): Tipo de vehículo, a elegir entre coche, moto o caravana.
- `matricula` (CharField, max_length=20, unique=True): Matrícula única del vehículo.
- `peso` (FloatField): Peso aproximado en kilogramos.
- `cliente` (ManyToManyField a Cliente, related_name="vehiculos"): Relación de cliente asociados.
- `marca` (CharField, max_length=25, null=True): Marca del vehículo, opcional.

### **Actividad**
Descripción: 
Actividades disponibles en el camping para los clientes.

Atributos:
- `nombre` (CharField, max_length=100): Nombre de la actividad.
- `descripcion` (TextField): Descripción detallada.
- `cupo` (PositiveIntegerField): Número máximo de participantes.
- `precio` (FloatField): Precio por persona.
- `requiere_material` (BooleanField, default=False): Indica si se necesita material específico para el desarrollo de la misma.

### **Reserva**
Descripción: 
Reservas realizadas por clientes para parcelas y actividades.

Atributos:
- `cliente` (ForeignKey a Cliente, on_delete=models.CASCADE): Cliente que realiza la reserva.
- `parcela` (ForeignKey a Parcela, on_delete=models.PROTECT): Parcela reservada.
- `fecha_inicio` (DateField): Fecha de inicio de la reserva.
- `fecha_fin` (DateField): Fecha de finalización.
- `actividades` (ManyToManyField a Actividad): Actividades reservadas.

### **ServiciosExtra**
Descripción: 
Servicios adicionales que se pueden contratar, como el desayuno, electricidad, o barbacoa.

Atributos:
- `nombre` (CharField, max_length=100): Nombre del servicio.
- `precio` (DecimalField, max_digits=6, decimal_places=2): Precio del servicio.
- `descripcion` (TextField, blank=True): Descripción opcional del servicio.
- `disponible` (BooleanField, default=True): Estado de disponibilidad.

### **ReservaExtra**
Descripción: 
Servicios extra asociados a una reserva.

Atributos:
- `reserva` (ForeignKey a Reserva, on_delete=models.CASCADE): Reserva principal.
- `servicios_extra` (ForeignKey a ServiciosExtra, on_delete=models.CASCADE): Servicio extra contratado.
- `cantidad_solicitada` (IntegerField, default=1): Cantidad de servicios solicitados. Por ejemplo si son 3 personas, pero solo 2 quieren desayunos, solo 2.
- `observaciones` (CharField, max_length=150, null=True, blank=True): Observaciones opcionales.

### **Factura**
Descripción:
Facturas emitidas por servicios extra.

Atributos:
- `reserva` (ForeignKey a ReservaExtra, on_delete=models.CASCADE): Reserva extra a la que corresponde la factura.
- `total` (DecimalField, max_digits=8, decimal_places=2): Importe total de la factura.
- `emitida_en` (DateTimeField, default=timezone.now): Fecha y hora de emisión.
- `pagado` (BooleanField, default=False): Estado del pago.


## Parámetros Utilizados
- `max_length`: Limita la longitud del texto.
- `unique`: Asegura que el valor sea único y no se repita.
- `default`: Establece un valor por defecto.
- `max_digits`: Indica un numero máximo de digitos en un campo.
- `decimal_places`: Ajusta los decimales de un número.
- `choices`: Selector entre valores establecidos .
- `validators`: Permite definir reglas personalizadas en los valores de un campo.
- `blank`: Define si el campo puede estar vacío.
- `null`: Indica si el campo puede ser nulo.
- `timezone.now`: Devuelve la fecha/hora actual.


## DIAGRAMA DE CLASES
![Diagrama del modelo Entidad-Relacion](diagrama/ModeloE_R_Camping.png)
