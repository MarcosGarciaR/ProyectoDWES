# ProyectoDWES
Este proyecto tratará sobre una página web dedicada en un sistema de gestión de campings.
Esta web permitirá administrar clientes, empleados, reservas, actividades y facturación.

## DEFINICIÓN DE LOS MODELOS
### **Persona** 
Descripción: 
Modelo base que contiene los atributos comunes para todos los usuarios del sistema (clientes, recepcionistas, cuidadores).

Atributos:
- `nombre`: Nombre de la persona.
- `apellido`: Apellido de la persona.
- `dni`: Documento Nacional de Identidad, identificador único.
- `fecha_nacimiento`: Fecha de nacimiento.
- `email`: Correo electrónico, único en la base de datos. Se utiliza el atributo EmailField que sirve para el control de estos.
- `telefono`: Número de teléfono del usuario.

### **PerfilUsuario**
Descripción: 
Perfil de usuario asociado a una persona para control de autenticación y permisos.

Atributos:
- `datos_usuario`: Relación uno a uno con Persona.
- `username`: Nombre de usuario único.
- `password`: Contraseña cifrada del usuario. Por ahora no tiene ningún control de carácteres.
- `es_staff`: Indica si el usuario pertenece a la administración. Para futuros permisos a trabajadores.
- `fecha_registro`: Fecha y hora de registro.



### **Recepcionista**
Descripción: 
Empleado de recepción en el camping.

Atributos:
- `usuario`: Usuario asignado al recepcionista.
- `salario`: Salario mensual. Con algunos controles lógicos.
- `fecha_alta`: Fecha en la que fue contratado.
- `turno`: Turno asignado (a elegir entre mañana o tarde).

### **Cuidador**
Descripción: 
Empleado encargado del cuidado de usuarios e instalaciones.

Atributos:
- `usuario`: Usuario de la web asignado al cuidador.
- `especialidad`: Área de especialización. 
- `disponible_de_noche`: Indica si está disponible por la noche.
- `puntuacion`: Valoración del cuidador de 1 a 10.

### **Cliente**
Descripción: 
Persona que utiliza los servicios del camping.

Atributos:
- `datos_cliente`: Datos personales asociados.
- `numero_cuenta`: Cuenta bancaria del cliente, puede estar en blanco (Una reserva de 5 personas, a nombre de un único cliente).
- `nacionalidad`: Nacionalidad del cliente.
- `acepta_publicidad`: Permiso para recibir publicidad.

### **Camping**
Descripción: 
Información general del camping.

Atributos:
- `nombre`: Nombre del camping.
- `ubicacion`: Dirección.
- `estrellas`: Clasificación por estrellas (1 a 5). Parámetro validators que permite únicamente los valores indicados.
- `sitio_web`: Página web oficial, opcional. Se utiliza el atributo URLField que permite agregar URLs (Aunque todos los campings se gestionen de manera "centralizada", cada uno de ellos debería tener su propia dirección web, o dentro de la misma, distintas rutas).

### **Parcela**
Descripción: 
Parcelas dentro del camping disponibles para reservar.

Atributos:
- `camping`: Camping en el que se encuentra la parcela.
- `numero`: Número identificador único de la parcela.
- `capacidad`: Capacidad máxima de personas, por defecto para 2 personas.
- `tiene_sombra`: Indica si la parcela tiene sombra (Para plus de precio).

### **Vehiculo**
Descripción: 
Vehículos registrados por los clientes.

Atributos:
- `tipo`: Tipo de vehículo, a elegir entre coche, moto o caravana.
- `matricula`: Matrícula única del vehículo.
- `peso`: Peso aproximado en kilogramos.
- `cliente`: Relación de cliente asociados.
- `marca`: Marca del vehículo, opcional.

### **Actividad**
Descripción: 
Actividades disponibles en el camping para los clientes.

Atributos:
- `nombre`: Nombre de la actividad.
- `descripcion`: Descripción detallada.
- `cupo`: Número máximo de participantes.
- `precio`: Precio por persona.
- `requiere_material`: Indica si se necesita material específico para el desarrollo de la misma.

### **Reserva**
Descripción: 
Reservas realizadas por clientes para parcelas y actividades.

Atributos:
- `cliente`: Cliente que realiza la reserva.
- `parcela`: Parcela reservada.
- `fecha_inicio`: Fecha de inicio de la reserva.
- `fecha_fin`: Fecha de finalización.
- `actividades`: Actividades reservadas.

### **ServiciosExtra**
Descripción: 
Servicios adicionales que se pueden contratar, como el desayuno, electricidad, o barbacoa.

Atributos:
- `nombre`: Nombre del servicio.
- `precio`: Precio del servicio.
- `descripcion`: Descripción opcional del servicio.
- `disponible`: Estado de disponibilidad.

### **ReservaExtra**
Descripción: 
Servicios extra asociados a una reserva.

Atributos:
- `reserva`: Reserva principal.
- `servicios_extra`: Servicio extra contratado.
- `cantidad_solicitada`: Cantidad de servicios solicitados. Por ejemplo si son 3 personas, pero solo 2 quieren desayunos, solo 2.
- `observaciones`: Observaciones opcionales.

### **Factura**
Descripción:
Facturas emitidas por servicios extra.

Atributos:
- `reserva`: Reserva extra a la que corresponde la factura.
- `total`: Importe total de la factura.
- `emitida_en`: Fecha y hora de emisión.
- `pagado`: Estado del pago.


## Parámetros Utilizados para la creación de los Modelos
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
- `help_text`: Nos permite agregar un texto de ayuda.


## Parámetros Utilizados para la generación de datos con Faker
- `chance_of_getting_true`: Permite indicar el porcentaje de que un boolean sea True.
- `random.randint`: Devuelve un numero entero mayor/igual y menor/igual que dos valores límite. 
- `random.uniform`: Devuelve un numero float mayor/igual y menor/igual que dos valores límite.
- `variable.{campo}.add`: Agrega (En mi caso, utilizado con v.cliente.add o re.servicios_extra.add).
- `round`: Redondea un número float, a unos decimales que se indiquen.
- `date_between_dates`: Agrega una fecha entre otras dos pasadas por parámetros.

## DIAGRAMA DE CLASES
![Diagrama del modelo Entidad-Relacion](diagrama/ModeloE_R_Camping.png)
