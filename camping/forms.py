from django import forms
from django.forms import ModelForm
from .models import *
from .forms import *
from datetime import date


from django.contrib.auth.forms import UserCreationForm



class RegistroForm(UserCreationForm):
    ROLES = (
        ("", "Seleccione un rol"),
        (Usuario.RECEPCIONISTA, 'Recepcionista'),
        (Usuario.CUIDADOR, 'Cuidador'),
        (Usuario.CLIENTE, 'Cliente'),
    )
    rol = forms.ChoiceField(choices=ROLES)
    
    salario = forms.DecimalField(required=False, label="Salario")
    turno = forms.ChoiceField(choices=Recepcionista.OPCIONES_TURNO, required=False, label="Turno")
    
    especialidad = forms.CharField(required=False, label="Especialidad")
    puntuacion = forms.DecimalField(required=False, label="Puntuación", min_value=1, max_value=10)
    
    numero_cuenta = forms.CharField(required=False, label="Número de cuenta")
    nacionalidad = forms.CharField(required=False, label="Nacionalidad")
    
    class Meta:
        model = Usuario
        fields = ("username", "email" , "password1", "password2","rol")
    
    def clean(self):
        super().clean()
        
        rol = self.cleaned_data.get('rol')
        
        salario = self.cleaned_data.get('salario')
        turno = self.cleaned_data.get('turno')
        
        especialidad = self.cleaned_data.get('especialidad')
        puntuacion = self.cleaned_data.get('puntuacion')
        
        numero_cuenta = self.cleaned_data.get('numero_cuenta')
        nacionalidad = self.cleaned_data.get('nacionalidad')
        
        if rol == "":
            self.add_error('rol', 'Debe seleccionar un rol válido')
        
        if rol == str(Usuario.RECEPCIONISTA):
            if salario is None or salario <= 0:
                self.add_error('salario', 'Debe introducir un salario válido para el recepcionista')
            
            if turno not in dict(Recepcionista.OPCIONES_TURNO):
                self.add_error('turno', 'Debe seleccionar un turno válido para el recepcionista')
        
        if rol == str(Usuario.CUIDADOR):
            if especialidad is None or especialidad.strip() == "":
                self.add_error('especialidad', 'Debe introducir una especialidad válida para el cuidador')
            
            if puntuacion is None or puntuacion < 1 or puntuacion > 10:
                self.add_error('puntuacion', 'La puntuación debe estar entre 1 y 10 para el cuidador')
                
        if rol == str(Usuario.CLIENTE):
            if numero_cuenta is None or numero_cuenta.strip() == "" or len(numero_cuenta) < 6:
                self.add_error('numero_cuenta', 'Debe introducir un número de cuenta válido para el cliente')
            
            if nacionalidad is None or nacionalidad.strip() == "":
                self.add_error('nacionalidad', 'Debe introducir una nacionalidad válida para el cliente')
                
                
        return self.cleaned_data


class PersonaModelForm(ModelForm):
    class Meta:
        model = Persona
        fields = '__all__'
        labels = {
            "nombre": ("Nombre de la persona"),
            "apellido": ("Apellidos"),
            'dni': ("DNI")
        }
        """WIDGETS => dar formato especial al campo"""
        widgets = {
            "fecha_nacimiento":forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        }
        
        """ 
        LOCALIZED_FIELDS => Para tener en cuenta la zona horaria en la creación de la fecha.        
        """
        localized_fields = ["fecha_nacimiento"]

    def clean(self):
        super().clean()
        
        nombre = self.cleaned_data.get('nombre')
        apellido = self.cleaned_data.get('apellido')
        dni = self.cleaned_data.get('dni')
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        telefono = self.cleaned_data.get('telefono')
        
        if len(nombre) < 3:
            self.add_error('nombre', 'El nombre es muy corto')
        if len(nombre) > 100:
            self.add_error('nombre', 'El nombre es muy largo')

        if len(apellido) < 3:
            self.add_error('apellido', 'El apellido es muy corto')
        if len(apellido) > 100:
            self.add_error('apellido', 'El apellido es muy largo')
            
        if len(dni) != 9:
            self.add_error('dni',"El formato del DNI no es correcto")
        
        miPersona = Persona.objects.filter(dni=dni).first()
        if (not (miPersona is None or (not self.instance is None and miPersona.id == self.instance.id )
                )
        ):
            self.add_error('dni', "Este DNI no está disponible")
            
        if fecha_nacimiento > date.today():
            self.add_error('fecha_nacimiento', 'La fecha de nacimiento no puede ser posterior a la fecha de hoy')
        
        
        """
        Telefono < 9 digitos (más si por +34 etc)
        Telefono, quitando 0, no sea vacío (no sea todo ceros)
        NO (Teléfono vacio O (objeto no es None y el ID de telefono es el de instancia)) == NO (False OR True) = NO (True) = False = No entra en el if
        """
        
        miTelefono = Persona.objects.filter(telefono = telefono).first()
        if len(telefono) < 9 or len(telefono) > 20 or telefono.strip("0") == "" or not (miTelefono is None or (not self.instance is None and miTelefono.id == self.instance.id ) ):
            self.add_error('telefono', 'El telefono es incorrecto')
        
        
        
        return self.cleaned_data


class BusquedaPersonasForm(forms.Form):
    nombreBusqueda = forms.CharField(required=False, label="Nombre")
    
    apellidosBusqueda = forms.CharField(required=False, label="Apellidos")

    dni = forms.CharField(required=False, label="DNI")

    annio_nacimiento = forms.IntegerField(required=False, label="Año de nacimiento")
    
    
    def clean(self):
        super().clean()
        
        nombreBusqueda = self.cleaned_data.get('nombreBusqueda')
        apellidosBusqueda = self.cleaned_data.get('apellidosBusqueda')
        dni = self.cleaned_data.get('dni')
        annio_nacimiento = self.cleaned_data.get('annio_nacimiento')
        
        if(nombreBusqueda == "" 
            and apellidosBusqueda == "" 
            and dni == "" 
            and annio_nacimiento is None
            ):
            self.add_error('nombreBusqueda', 'Debe introducir al menos un campo de busqueda')
            self.add_error('apellidosBusqueda', 'Debe introducir al menos un campo de busqueda')
            self.add_error('dni', 'Debe introducir al menos un campo de busqueda')
            self.add_error('annio_nacimiento', 'Debe introducir al menos un campo de busqueda')
        
        else:
            annioActual = date.today().year
    
            if(nombreBusqueda != "" and len(nombreBusqueda) < 3):
                self.add_error('nombreBusqueda', 'El nombre es demasiado corto')
            
            if(apellidosBusqueda != "" and len(apellidosBusqueda) < 3):
                self.add_error('apellidosBusqueda', 'El apellido es demasiado corto')
            
            if(dni != "" and (len(dni) < 8 or len(dni) > 10)):
                self.add_error('dni', "El DNI no es correcto")
                
            if(annio_nacimiento  is not None and ( annio_nacimiento < 0 or annio_nacimiento > annioActual)):
                self.add_error("annio_nacimiento", "El año de nacimiento no es válido")
                
        return self.cleaned_data




## RECEPCIONISTA
class RecepcionistaModelForm(ModelForm):
    class Meta:
        model = Recepcionista
        # Iba a poner que la fecha de alta sea automática, pero se puede dar de alta a usuarios que ya están en plantilla (Entra hoy pero se le dan permisos al dia siguiente por ej)
        fields = '__all__'
        widgets = {
            "salario": forms.NumberInput(attrs={'type': 'number'}),
            "fecha_alta": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "turno": forms.Select(attrs={"class": "form-control"}),
        }
        localized_fields = ["fecha_alta"]

    def clean(self):
        super().clean()

        salario = self.cleaned_data.get('salario')
        fecha_alta = self.cleaned_data.get('fecha_alta')
        turno = self.cleaned_data.get('turno')

        if salario is not None and salario < 0:
            self.add_error("salario", "El salario no puede ser negativo")
        if salario == "":
            self.add_error("salario", "Debe introducir un salario")
        
        if fecha_alta is not None and fecha_alta > date.today():
            self.add_error("fecha_alta", "La fecha de alta no puede ser futura")

        if turno not in ('ma', 'ta'):
            self.add_error("turno", "Por favor, seleccione un turno válido")

        return self.cleaned_data


class BusquedaRecepcionistasForm(forms.Form):

    salario = forms.DecimalField(required=False, label="Salario")
    fecha_desde = forms.DateField(label="Alta Desde",required=False,widget= forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}))        
    fecha_hasta = forms.DateField(label="Alta Hasta",required=False,widget= forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}))
    
    turno = forms.MultipleChoiceField(choices=Recepcionista.OPCIONES_TURNO ,required=False,widget=forms.CheckboxSelectMultiple())

    def clean(self):
        super().clean()

        salario = self.cleaned_data.get('salario')
        fecha_desde = self.cleaned_data.get('fecha_desde')
        fecha_hasta = self.cleaned_data.get('fecha_hasta')
        turno = self.cleaned_data.get('turno')

        if (salario is None and fecha_desde is None and fecha_hasta is None and not turno):
            msg = "Debe introducir al menos un campo de búsqueda"
            self.add_error('salario', msg)
            self.add_error('fecha_desde', msg)
            self.add_error('fecha_hasta', msg)
            self.add_error('turno', msg)
        
        else:
            if (salario is not None and salario < 0):
                self.add_error("salario", "El salario no puede ser negativo")

            if(not fecha_desde is None  and not fecha_hasta is None and fecha_hasta < fecha_desde):
                self.add_error('fecha_desde','La fecha hasta no puede ser menor que la fecha desde')
                self.add_error('fecha_hasta','La fecha hasta no puede ser menor que la fecha desde')
                
            if (not fecha_desde is None and fecha_desde > date.today()):
                self.add_error("fecha_desde", "La fecha de registro no puede ser superior a la fecha actual")

        return self.cleaned_data

# FORMS CAMPING
## CREATE
class CampingModelForm(ModelForm):
    class Meta:
        model = Camping
        fields = '__all__'
        labels = {
            "nombre": ("Nombre del camping"),
            "ubicacion": ("Ubicación"),
            "estrellas": ("Número de estrellas"),
            "sitio_web": ("Sitio web oficial"),
        }
        widgets = {
            "estrellas": forms.NumberInput(attrs={"class": "form-control","min": 1,"max": 5}),
            "sitio_web": forms.URLInput(attrs={"class": "form-control","placeholder": "https://ejemplo.com"}),
            }
        
        
    def clean(self):
        super().clean()
        
        nombre = self.cleaned_data.get('nombre')
        ubicacion = self.cleaned_data.get('ubicacion')
        estrellas = self.cleaned_data.get('estrellas')
        sitio_web = self.cleaned_data.get('sitio_web')

        if len(nombre) < 3:
            self.add_error('nombre', 'El nombre es demasiado corto')
        if len(nombre) > 150:
            self.add_error('nombre', 'El nombre es demasiado largo')

        if len(ubicacion) < 10:
            self.add_error('ubicacion', 'La ubicación es demasiado corta')
        if len(ubicacion) > 200:
            self.add_error('ubicacion', 'La ubicación es demasiado larga')

        if estrellas is not None and estrellas < 1 or estrellas > 5:
                self.add_error('estrellas', 'El número de estrellas debe estar entre 1 y 5')

        if sitio_web:
            if not sitio_web.startswith("http"):
                self.add_error('sitio_web', 'La URL debe comenzar por http:// o https://')

        return self.cleaned_data


## READ
class BusquedaCampingsForm(forms.Form):
    nombre = forms.CharField(required=False, label="Nombre")
    ubicacion = forms.CharField(required=False, label="Ubicación")
    estrellas = forms.DecimalField(required=False, label="Mínimo de estrellas (puntuación) 1-5")
    sitio_web = forms.CharField(required=False, label="URL de la web del camping")
    
    def clean(self):
        super().clean()
        
        nombre = self.cleaned_data.get('nombre')
        ubicacion = self.cleaned_data.get('ubicacion')
        estrellas = self.cleaned_data.get('estrellas')
        sitio_web = self.cleaned_data.get('sitio_web')

        if(nombre == "" and ubicacion == "" and estrellas is None and sitio_web == ""):
            msg = "Debe introducir al menos un campo de búsqueda"
            self.add_error('nombre', msg)
            self.add_error('ubicacion', msg)
            self.add_error('estrellas', msg)
            self.add_error('sitio_web', msg)
            
        else:
            if( nombre != "" and len(nombre) < 5):
                self.add_error('nombre', 'El nombre del camping es demasiado corto')
            elif nombre != "" and len(nombre)> 150:
                self.add_error('nombre', 'El nombre del camping es demasiado largo')
            
            if( ubicacion != "" and len(ubicacion) < 5):
                self.add_error('ubicacion', 'El nombre del camping es demasiado corto')
            elif ubicacion != ""and len(ubicacion) > 200:
                self.add_error('ubicacion', 'El nombre del camping es demasiado largo')
            
            if(estrellas is not None and (estrellas > 5 or estrellas < 1)):
                self.add_error('estrellas', 'Número de estrellas no válido' )
    
            if sitio_web != "" and len(sitio_web) < 4:
                self.add_error('sitio_web', 'La descripción proporcionada para el sitio web es demasiado corta')
    
        return self.cleaned_data


# FORMS PARCELA
class ParcelaModelForm(ModelForm):
    class Meta:
        model = Parcela
        fields = '__all__'
        labels = {
            "camping": ("Camping"),
            "numero": ("Número de parcela"),
            "capacidad": ("Capacidad de personas"),
            "tiene_sombra": ("¿Tiene sombra?"),       
        }
        
        widgets = {
            "camping": forms.Select(attrs={"class": "form-control"}),
            "numero": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "capacidad": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 25}),
            "tiene_sombra": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean(self):
        super().clean()

        numero = self.cleaned_data.get('numero')
        capacidad = self.cleaned_data.get('capacidad')
        camping = self.cleaned_data.get('camping')

        if numero is None or numero < 1:
                self.add_error('numero', 'El número de parcela debe ser mayor que 0')
    
        if capacidad is not None and capacidad < 1:
            self.add_error('capacidad', 'La capacidad debe ser al menos 1 persona')
            
        if capacidad is not None and capacidad > 25:
            self.add_error('capacidad', 'La capacidad máxima es de 25 personas')
            
        if capacidad is None:
            self.add_error('capacidad', 'Debe introducir alguna capacidad')
            # En el camping ya puede haber una parcela que tenga el numero indicado, en ese caso debería saltar error también.
        if camping and numero:
            parcela_existente = Parcela.objects.filter(camping=camping, numero=numero).first()
            if parcela_existente and (self.instance is None or parcela_existente.id != self.instance.id):
                        self.add_error('numero', 'Ya existe una parcela con ese número en este camping')


        return self.cleaned_data


class BusquedaParcelasForm(forms.Form):
    numero = forms.IntegerField(required=False, label="Número de parcela")
    capacidad = forms.IntegerField(required=False, label="Capacidad máxima de personas")
    tiene_sombra = forms.NullBooleanField(required=False, label="¿Tiene sombra?")
    nombre_camping = forms.CharField(required=False, label="Nombre del camping")
    
    def clean(self):
        super().clean()
        
        numero = self.cleaned_data.get('numero')
        capacidad = self.cleaned_data.get('capacidad')
        tiene_sombra = self.cleaned_data.get('tiene_sombra')
        nombre_camping = self.cleaned_data.get('nombre_camping')

        if numero is None and capacidad is None and tiene_sombra is None and nombre_camping == "":
            msg = "Debe introducir al menos un campo de búsqueda"
            self.add_error('numero', msg)
            self.add_error('capacidad', msg)
            self.add_error('tiene_sombra', msg)
            self.add_error('nombre_camping', msg)
        else:
            
            if numero is not None and numero < 1:
                self.add_error('numero', 'El número de parcela debe ser mayor que 0')
            
            if capacidad is not None and capacidad < 1:
                self.add_error('capacidad', 'La capacidad mínima debe ser al menos 1 persona')
            
            if nombre_camping != "" and len(nombre_camping) < 3:
                self.add_error('nombre_camping', 'El nombre del camping es demasiado corto')
            elif nombre_camping != "" and len(nombre_camping) > 150:
                self.add_error('nombre_camping', 'El nombre del camping es demasiado largo')
        
        return self.cleaned_data
    
    
# FORMS FACTURA
class FacturaModelForm(ModelForm):
    class Meta:
        model = Factura
        fields = '__all__'
        labels = {
            "reserva_extra": ("Reserva Extra"),
            "total": ("Total (€)"),
            "emitida_en": ("Emitida en"),
            "pagado": ("Pagado"),
        }
        widgets = {
            "reserva_extra": forms.Select(attrs={"class": "form-control"}),
            "total": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "emitida_en":forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "pagado": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        localized_fields = ["emitida_en"]
        
    def clean(self):
        super().clean()

        emitida_en = self.cleaned_data.get('emitida_en')
        total = self.cleaned_data.get('total')
        reserva_extra = self.cleaned_data.get('reserva_extra')

        # Validación de total
        if total is None:
            self.add_error('total', 'Debe indicar un total')
        elif total < 0:
            self.add_error('total', 'El total no puede ser negativo')

        if emitida_en.date() > date.today():
            self.add_error('emitida_en', 'La fecha de emisión no puede ser posterior a la fecha de hoy')
        
        if reserva_extra:
            qs = Factura.objects.filter(reserva_extra=reserva_extra)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                self.add_error('reserva_extra', 'Ya existe una factura para esta reserva extra')

        return self.cleaned_data


class BusquedaFacturasForm(forms.Form):
    reserva_extra = forms.IntegerField(required=False, label="ID de Reserva Extra")
    pagado = forms.NullBooleanField(required=False, label="¿Pagado?")
    fecha_inicio = forms.DateField(required=False, label="Emitida desde", widget=forms.DateInput(attrs={"type": "date"}))
    fecha_fin = forms.DateField(required=False, label="Emitida hasta", widget=forms.DateInput(attrs={"type": "date"}))

    def clean(self):
        super().clean()
        
        reserva_extra = self.cleaned_data.get('reserva_extra')
        pagado = self.cleaned_data.get('pagado')
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        fecha_fin = self.cleaned_data.get('fecha_fin')

        if reserva_extra is None and pagado is None and not fecha_inicio and not fecha_fin:
            msg = "Debe introducir al menos un campo de búsqueda"
            self.add_error('reserva_extra', msg)
            self.add_error('pagado', msg)
            self.add_error('fecha_inicio', msg)
            self.add_error('fecha_fin', msg)

        if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
            self.add_error('fecha_fin', 'La fecha fin debe ser mayor o igual que la fecha de inicio')

        return self.cleaned_data


# FORMS RESERVA
class ReservaModelForm(ModelForm):
    class Meta:
        model = Reserva
        fields = '__all__'
        widgets = {
            "fecha_inicio": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "fecha_fin": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "actividades": forms.CheckboxSelectMultiple(),
            "cliente": forms.Select(attrs={"class": "form-control"}),
            "parcela": forms.Select(attrs={"class": "form-control"}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ReservaModelForm, self).__init__(*args, **kwargs)

        if self.user and self.user.rol == Usuario.CLIENTE:
            # Si es cliente, el campo cliente se asigna dinámicamente (está oculto a la vista del usuario)
            if hasattr(self.user, 'cliente'):
                 self.fields['cliente'].queryset = Cliente.objects.filter(id=self.user.cliente.id)
                 self.fields['cliente'].initial = self.user.cliente
        
    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        
        if fecha_inicio and fecha_fin:
            if fecha_inicio > fecha_fin:
                self.add_error('fecha_fin', 'La fecha fin debe ser posterior a la de inicio')
            
            if fecha_inicio < date.today():
                self.add_error('fecha_inicio', 'La fecha de inicio no puede ser anterior a la fecha de hoy')

        return cleaned_data
