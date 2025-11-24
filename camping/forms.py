from django import forms
from django.forms import ModelForm
from .models import *
from .forms import *
from django.contrib import messages


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
            "apellido": ("Apellidos"),
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
        
        nombre = self.cleaned_data('nombre')
        apellido =  self.cleaned_data('apellido')
        dni =  self.cleaned_data('dni')
        fecha_nacimiento =  self.cleaned_data('fecha_nacimiento')
        email =  self.cleaned_data('email')
        telefono =  self.cleaned_data('telefono')
        
        if len(dni) != 9:
            self.add_error('dni',"El DNI no es correcto")
        
        miDNI = Persona.objects.get(dni = dni)
        if (not miDNI is None):
            self.add_error('dni', "Este DNI ya existe")
            
            
        return self.cleaned_data



