from django.urls import path
from .api_views import *

urlpatterns = [
    path('reservas', reserva_list),
    path('reservas_mejoradas', reservas_mejoradas_list),
]