from django.urls import path, re_path
from .import views

urlpatterns = [
    path('', views.index , name='index'),
    path('campings/', views.ver_campings , name='ver_campings'),
    path('reservas/', views.ver_reservas_por_fecha , name='ver_reservas'),
    path('reservaid/<int:id_reserva>/', views.ver_reserva_por_id , name='ver_reserva_por_id'),
    path('factura-coste/<int:precio>/<int:capacidadParcela>/', views.ver_factura_precio_capacidad , name='ver_facturas'),
    path('servicios/', views.precio_medio_servicios , name='precio_medio_servicios'),
    path('cuidadores/<int:puntuacionPedida>/', views.puntuacionydisponibilidad_cuidadores , name='cuidadores_puntuacion_disponibilidad'),
    path('serviciosextra/<str:texto>/', views.busqueda_descripcion_serviciosextra , name='descripcion_serviciosextra'),
    re_path(r"^cliente[0-9]$", views.clientes_sin_vehiculo , name='clientes_sin_vehiculo'),
    re_path(r"^reserva[0-9]$", views.reservas_sin_actividades , name='reservas_sin_actividades'),
    path('cliente/<int:cliente_id>/reservas/', views.reservas_de_cliente_por_id , name='reservas_de_cliente_por_id'),
    
    path('recepcionistas/', views.prueba_clase , name='prueba_clase'),
]

