from django.shortcuts import render
from .models import *
# from django.db.models import Q, Prefetch
# from django.views.defaults import page_not_found


# Create your views here.

def index(request):
    return render(request, 'index.html') 

def ver_campings(request):
    campings = Camping.objects.all()
    #campings = (Camping.objects.raw(" SELECT * FROM camping_camping c"))
    
    return render(request, 'URLs/campings.html', {"mostrar_campings":campings})

def ver_reservas_por_fecha(request):
    
