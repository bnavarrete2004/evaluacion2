# Api_Clinica/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EspecialidadViewSet,
    MedicoViewSet,
    PacienteViewSet,
    ConsultaMedicaViewSet,
    TratamientoViewSet,
    MedicamentoViewSet,
    RecetaMedicaViewSet
)

# Creamos un router para registrar nuestros ViewSets
# DefaultRouter nos proporciona automáticamente las URLs para los listados y detalles
router = DefaultRouter()
router.register(r'especialidades', EspecialidadViewSet)
router.register(r'medicos', MedicoViewSet)
router.register(r'pacientes', PacienteViewSet)
router.register(r'consultas', ConsultaMedicaViewSet)
router.register(r'tratamientos', TratamientoViewSet)
router.register(r'medicamentos', MedicamentoViewSet)
router.register(r'recetas', RecetaMedicaViewSet)

# Las URLs generadas por el router se incluyen en urlpatterns
urlpatterns = [
    path('', include(router.urls)),
]