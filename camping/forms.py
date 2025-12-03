from django import forms
from django.forms import ModelForm
from .models import *
from .forms import *
from datetime import date

## FORMS PERSONA
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
            "email":forms.EmailInput(attrs={"class": "form-control","placeholder":"ejemplo@correo.com"}),
            
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
        email = self.cleaned_data.get('email')
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
        
        miEmail = Persona.objects.filter(email=email).first()
        if (not (miEmail is None or (not self.instance is None and miEmail.id == self.instance.id )
                )
        ):
            self.add_error('email', "Este email no está disponible")
        
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


## PERFILUSUARIO CON FOTO DE PERFIL
# FORMS PERFIL USUARIO
class PerfilUsuarioModelForm(ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['datos_usuario', 'username', 'password', 'foto_perfil', 'es_staff', 'rol']
        labels = {
            "username": ("Nombre de usuario"),
            "password": ("Contraseña"),
            "rol": ("Rol del usuario"),
            "es_staff": ("¿Es staff?")
        }
        widgets = {
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "rol": forms.Select(attrs={"class": "form-control"}),
            "es_staff": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "foto_perfil": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # ✅ SOLO personas sin perfil de usuario
            self.fields['datos_usuario'].queryset = Persona.objects.filter(perfilusuario__isnull=True).order_by('nombre', 'apellido')
            
            # ✅ SOLO en EDICIÓN (UPDATE) incluir la persona actual
            if self.instance and self.instance.pk:  # Verificar que existe instancia
                self.fields['datos_usuario'].queryset |= Persona.objects.filter(id=self.instance.datos_usuario.id)
                
    def clean(self):
        super().clean()
        
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if len(username) < 3:
            self.add_error('username', 'El username debe tener al menos 3 caracteres')
        if len(username) > 50:
            self.add_error('username', 'El username no puede exceder 50 caracteres')
            
        if len(password) < 8:
            self.add_error('password', 'La contraseña debe tener al menos 8 caracteres')
            
        # Username único
        usuario_username = PerfilUsuario.objects.filter(username=username).exclude(id=self.instance.id if self.instance else None).first()
        if usuario_username:
            self.add_error('username', 'Este username ya está en uso')
            
        return self.cleaned_data


""" PARA EL UPDATE
    En el update, no se debe poder cambiar la persona de la relacion OneToOne, para ello
    lo más sencillo es crear otro formulario quitando este campo y listo.
"""
    
class PerfilUsuarioUpdateForm(ModelForm): 
    class Meta:
        model = PerfilUsuario
        fields = ['username', 'password', 'foto_perfil', 'es_staff', 'rol']  
        labels = {
            "username": ("Nombre de usuario"),
            "password": ("Contraseña"),
            "rol": ("Rol del usuario"),
            "es_staff": ("¿Es staff?")
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
            "es_staff": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "rol": forms.Select(attrs={"class": "form-control"}),
            "foto_perfil": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
        
    def clean(self):
        super().clean()
        
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if len(username) < 3:
            self.add_error('username', 'El username debe tener al menos 3 caracteres')
        if len(username) > 50:
            self.add_error('username', 'El username no puede exceder 50 caracteres')
            
        if len(password) < 8:
            self.add_error('password', 'La contraseña debe tener al menos 8 caracteres')
            
        usuario_username = PerfilUsuario.objects.filter(username=username).exclude(id=self.instance.id if self.instance else None).first()
        if usuario_username:
            self.add_error('username', 'Este username ya está en uso')
            
        return self.cleaned_data
        
        
class BusquedaPerfilesUsuariosForm(forms.Form):
    
    usernameBusqueda = forms.CharField(required=False, label="Username")
    rolBusqueda = forms.MultipleChoiceField(required=False, label="Rol", choices=PerfilUsuario.OPCIONES_ROL, widget = forms.CheckboxSelectMultiple())
    esStaffBusqueda = forms.BooleanField(required=False, label="Es Staff", widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    fecha_desde = forms.DateField(label="Registro Desde",required=False,widget= forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}))        
    fecha_hasta = forms.DateField(label="Registro Hasta",required=False,widget= forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}))
    
    def clean(self):
        super().clean()
        
        usernameBusqueda = self.cleaned_data.get('usernameBusqueda')
        rolBusqueda = self.cleaned_data.get('rolBusqueda')
        esStaffBusqueda = self.cleaned_data.get('esStaffBusqueda')
        fecha_desde = self.cleaned_data.get('fecha_desde')
        fecha_hasta = self.cleaned_data.get('fecha_hasta')


        if(usernameBusqueda == "" and rolBusqueda == "" and esStaffBusqueda is None and fecha_desde is None and fecha_hasta is None):
            self.add_error('usernameBusqueda', 'Debe introducir al menos un campo de búsqueda')
            self.add_error('fecha_desde','Debe introducir al menos un campo de búsqueda')
            self.add_error('fecha_hasta','Debe introducir al menos un campo de búsqueda')
        else:
            if(usernameBusqueda != "" and len(usernameBusqueda) < 3):
                self.add_error('usernameBusqueda', 'El username es demasiado corto')
            
            if(not fecha_desde is None  and not fecha_hasta is None and fecha_hasta < fecha_desde):
                self.add_error('fecha_desde','La fecha hasta no puede ser menor que la fecha desde')
                self.add_error('fecha_hasta','La fecha hasta no puede ser menor que la fecha desde')
                
            if (not fecha_desde is  None and fecha_desde > date.today()):
                self.add_error("fecha_desde", "La fecha de registro no puede ser superior a la fecha actual")
                
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

        # --- Validación salario ---
        if salario is not None and salario < 0:
            self.add_error("salario", "El salario no puede ser negativo")

        # --- Validación fecha ---
        if fecha_alta is not None and fecha_alta > date.today():
            self.add_error("fecha_alta", "La fecha de alta no puede ser futura")

        # --- Validación turno ---
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

    
    
# POR HACER  camping parcela  reserva 