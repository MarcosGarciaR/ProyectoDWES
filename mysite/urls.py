"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include 

## PARA LAS IMAGENES DE PERFIL DE LOS USUARIOS
from django.conf import settings
from django.conf.urls.static import static


from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include("debug_toolbar.urls")),
    
    # Password Reset Custom Templates
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/cambio_contrasenia_form.html'), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/cambio_contrasenia_hecho.html'), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/cambio_contrasenia_confirmar.html'), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/cambio_contrasenia_completado.html'), name='password_reset_complete'),
    
    path('accounts/password_reset/',auth_views.PasswordResetView.as_view(template_name='registration/cambio_contrasenia_form.html',email_template_name='registration/cambio_contrasenia_email.html'),name='password_reset'),


    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('camping.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



from django.conf.urls import handler404, handler400, handler403, handler500
handler404 = "camping.views.mi_error_404"
handler400 = "camping.views.mi_error_400"
handler403 = "camping.views.mi_error_403"
handler500 = "camping.views.mi_error_500"