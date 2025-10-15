from django.contrib import admin
from django.urls import path, include # Asegúrate de que 'include' esté importado
from rest_framework import permissions # Para la documentación de la API
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuración para la documentación de la API con drf-yasg 
schema_view = get_schema_view(
   openapi.Info(
      title="API Salud Vital Ltda.",
      default_version='v1',
      description="Documentación de la API para la gestión de pacientes, médicos y atenciones de Salud Vital Ltda.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@saludvital.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    # Incluye las URLs de tu aplicación Api_Clinica bajo el prefijo 'api/'
    path('api/', include('Api_Clinica.urls')),
    # URLs para las vistas HTML (las colocamos directamente en la raíz para simplicidad de navegación)
    path('', include('Api_Clinica.web_urls')),

    # URLs para la documentación de la API (drf-yasg)
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]