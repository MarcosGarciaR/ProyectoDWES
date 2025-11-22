from django import forms
from django.forms import ModelForm
from .models import *



class PersonaModelForm(ModelForm):
    class Meta:
        nombre = Persona
        fields = ['__all__']
        labels = {
            "nombre": ("Nombre de la persona"),
            "apellido": ("Apellidos"),
            
        }
        
        """WIDGETS => dar formato especial al campo"""
        widgets = {
            "email":forms.EmailInput()
            }       
        
        """ 
        LOCALIZED_FIELDS => Para tener en cuenta la zona horaria en la creación de la fecha.        
        """
        localized_fields = ["fecha_nacimiento"]


