from django import forms
from django.forms import ModelForm
from .models import *
from .forms import *
from datetime import date


"""
class PersonaForm(forms.Form):
    nombre = forms.CharField(label="Nombre", required=True, max_length=200, help_text="Máximo de 200 carácteres")
    
    apellido = forms.CharField(label="Apellidos", required=True, max_length=400, help_text="Máximo 400 carácteres")
    
    dni = forms.CharField(label="DNI", required=True, max_length=9, help_text="Máximo 9 carácteres")
    
    fecha_nacimiento = forms.DateField(label="Fecha de Nacimiento", )
    
    email = 
    
    telefono = 
    
"""
## PERSONA
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

class PerfilUsuarioModelForm(ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = '__all__'
        labels = {
            "username": "Nombre de usuario",
            "password": "Contraseña",
            'foto_perfil': "Foto de Perfil"
        }
        widgets = {
            'password': forms.PasswordInput(),
            'es_staff': forms.CheckboxInput(),
            'fecha_registro': forms.HiddenInput(),
            'foto_perfil': forms.FileInput(attrs={'accept': 'image/*'}),
        }
        localized_fields = ["fecha_registro"]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar personas que aún no tienen perfil
        # Si estamos editando, incluir la persona asociada actual
        if self.instance and self.instance.pk:
            self.fields['datos_usuario'].queryset = Persona.objects.filter(
                models.Q(perfilusuario__isnull=True) | models.Q(pk=self.instance.datos_usuario.pk)
            )
        else:
            self.fields['datos_usuario'].queryset = Persona.objects.filter(perfilusuario__isnull=True)
            
    def clean(self):
        super().clean()

        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        datos_usuario = self.cleaned_data.get('datos_usuario')

        if username:
            if len(username) < 3:
                self.add_error('username', 'El nombre de usuario es demasiado corto')
            elif len(username) > 50:
                self.add_error('username', 'El nombre de usuario es demasiado largo')

            miUsername = PerfilUsuario.objects.filter(username=username).first()
            if miUsername and (not self.instance or miUsername.id != self.instance.id):
                self.add_error('username', 'Este nombre de usuario no está disponible')

        # --- Validación de password ---
        if password:
            if len(password) < 6:
                self.add_error('password', 'La contraseña es demasiado corta')
        else:
            self.add_error('password', 'Debe ingresar una contraseña')

        # --- Validación de datos_usuario ---
        disponibles_qs = Persona.objects.filter(perfilusuario__isnull=True)

        if self.instance and self.instance.pk and self.instance.datos_usuario:
            disponibles_qs = disponibles_qs | Persona.objects.filter(pk=self.instance.datos_usuario.pk)

        if not disponibles_qs.exists():
            self.add_error('datos_usuario', 'No hay personas disponibles para asignar un perfil de usuario.')
        elif datos_usuario:
            if datos_usuario not in disponibles_qs:
                self.add_error('datos_usuario', 'La persona seleccionada ya tiene un perfil de usuario.')
        else:
            self.add_error('datos_usuario', 'Debe seleccionar una persona para asignar el perfil de usuario.')

        return self.cleaned_data


class BusquedaPerfilesUsuarioForm(forms.Form):
    username = forms.CharField(required=False, label="Nombre de usuario")
    es_staff = forms.CheckboxInput()
    rol = forms.ChoiceField(choices=['recepcionista', 'cuidador', 'cliente'], required=False, label="ROL")
    fecha_registro = forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"})
    
    def clean(self):
        super().clean()
        
        username = self.cleaned_data.get('username')
        es_staff = self.cleaned_data.get('es_staff')
        rol = self.cleaned_data.get('rol')
        fecha_registro = self.cleaned_data.get('fecha_registro')
        
        if(username == "" 
            and es_staff == "" 
            and rol == "" 
            and fecha_registro 
            ):
            self.add_error('username', 'Debe introducir al menos un campo de busqueda')
            self.add_error('es_staff', 'Debe introducir al menos un campo de busqueda')
            self.add_error('rol', 'Debe introducir al menos un campo de busqueda')
            self.add_error('fecha_registro', 'Debe introducir al menos un campo de busqueda')
            
        else:
    
            if(username != "" and len(username) < 3):
                self.add_error('nombreBusqueda', 'El nombre es demasiado corto')
                
            if fecha_registro > date.today():
                self.add_error('fecha_registro', 'La fecha de registro no puede ser posterior a la fecha de hoy')
                
        return self.cleaned_data



