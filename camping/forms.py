from django import forms
from django.forms import ModelForm
from .models import *



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
        nombre = Persona
        fields = ['__all__']
        labels = {
            "nombre": ("Nombre de la persona"),
            "apellido": ("Apellidos"),
            
        }
        """WIDGETS => dar formato especial al campo"""
        
        
        
        """ 
        LOCALIZED_FIELDS => Para tener en cuenta la zona horaria en la creación de la fecha.        
        """
        localized_fields = ["fecha_nacimiento"]






