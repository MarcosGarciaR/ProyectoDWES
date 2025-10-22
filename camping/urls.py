from django.urls import path
from .import views

urlpatterns = [
    path('', views.index , name='index'),
    path('campings/', views.ver_campings , name='ver_campings'),
    path('reservas/', views.ver_reservas_por_fecha , name='ver_reservas'),
    
    
]

