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

class PersonaModelForm(ModelForm):
    class Meta:
        model = Persona
        fields = '__all__'
        labels = {
            "nombre": ("Nombre de la persona"),
            "apellido": ("Apellidos")
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
        email = self.cleaned_data.get('email')
        telefono = self.cleaned_data.get('telefono')
        
        if len(nombre) < 3:
            self.add_error('nombre', 'El nombre es muy corto')
        
        if len(apellido) < 3:
            self.add_error('nombre', 'El nombre es muy corto')
        
        if len(dni) != 9:
            self.add_error('dni',"El formato del DNI no es correcto")
        
        miDNI = Persona.objects.filter(dni=dni).first()
        if (not miDNI is None):
            self.add_error('dni', "Este DNI no está disponible")
            
        if fecha_nacimiento > date.today():
            self.add_error('fecha_nacimiento', 'La fecha de nacimiento no puede ser posterior a la fecha de hoy')
        
        miEmail = Persona.objects.filter(email=email).first()
        if(not miEmail is None):
            self.add_error('email', "Este email no está disponible")
        
        miTelefono = Persona.objects.filter(telefono = telefono).first()
        if len(telefono) < 9 or telefono == 0 or (not miTelefono is None):
            self.add_error('telefono', 'El telefono es incorrecto')
            
        return self.cleaned_data



