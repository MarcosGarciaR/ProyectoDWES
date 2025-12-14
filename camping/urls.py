from django.urls import path, re_path
from .import views

urlpatterns = [
    path('', views.index , name='index'),
    path('reservaid/<int:id_reserva>/', views.ver_reserva_por_id , name='ver_reserva_por_id'),
    path('factura-coste/<int:precio>/<int:capacidadParcela>/', views.ver_factura_precio_capacidad , name='ver_facturas_especial'),
    path('servicios/', views.precio_medio_servicios , name='precio_medio_servicios'),
    path('cuidadores/<int:puntuacionPedida>/', views.puntuacionydisponibilidad_cuidadores , name='cuidadores_puntuacion_disponibilidad'),
    path('serviciosextra/<str:texto>/', views.busqueda_descripcion_serviciosextra , name='descripcion_serviciosextra'),
    re_path(r"^cliente[0-9]$", views.clientes_sin_vehiculo , name='clientes_sin_vehiculo'),
    re_path(r"^reserva[0-9]$", views.reservas_sin_actividades , name='reservas_sin_actividades'),
    path('cliente/<int:cliente_id>/reservas/', views.reservas_de_cliente_por_id , name='reservas_de_cliente_por_id'),
    
    
    
    # FORMS
    
    path('personas/', views.ver_personas, name='ver_personas'),
    path('formulario_persona/', views.crear_persona , name='crear_persona'),
    path('busqueda_personas/', views.buscar_personas, name='buscar_personas'),
    path('persona/editar/<int:persona_id>', views.persona_editar, name='editar_persona'),
    path('persona/eliminar/<int:persona_id>', views.persona_eliminar, name='eliminar_persona'),
    
    
    
    path('recepcionistas/', views.ver_recepcionistas , name='ver_recepcionistas'),
    path('formulario_recepcionista', views.crear_recepcionista, name="crear_recepcionista"),
    path('busqueda_recepcionistas', views.buscar_recepcionistas, name="buscar_recepcionistas"),
    path('recepcionista/editar/<int:recepcionista_id>', views.recepcionista_editar, name='editar_recepcionista'),
    path('recepcionista/eliminar/<int:recepcionista_id>', views.recepcionista_eliminar, name='eliminar_recepcionista'),
    
    
    path('campings/', views.ver_campings , name='ver_campings'),
    path('formulario_camping/', views.crear_camping , name='crear_camping'),
    path('busqueda_campings', views.buscar_campings, name="buscar_campings"),
    path('camping/editar/<int:camping_id>', views.camping_editar, name='editar_camping'),
    path('camping/eliminar/<int:camping_id>', views.camping_eliminar, name='eliminar_camping'),
    
    path('parcelas/', views.ver_parcelas, name="ver_parcelas"),
    path('formulario_parcela/', views.crear_parcela , name='crear_parcela'),
    path('busqueda_parcelas', views.buscar_parcelas, name="buscar_parcelas"),
    path('parcela/editar/<int:parcela_id>', views.parcela_editar, name='editar_parcela'),
    path('parcela/eliminar/<int:parcela_id>', views.parcela_eliminar, name='eliminar_parcela'),
    
    path('facturas/', views.ver_facturas, name="ver_facturas"),
    path('formulario_factura/', views.crear_factura , name='crear_factura'),
    path('busqueda_facturas', views.buscar_facturas, name="buscar_facturas"),
    path('factura/editar/<int:factura_id>', views.factura_editar, name='editar_factura'),
    path('factura/eliminar/<int:factura_id>', views.factura_eliminar, name='eliminar_factura'),
    
    
    path('reservas/', views.ver_reservas_por_fecha , name='ver_reservas'),
    path('formulario_reserva/', views.crear_reserva , name='crear_reserva'),
    

    path('registrar', views.registrar_usuario, name='registrar_usuario'),
    
]




