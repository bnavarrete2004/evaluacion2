# Api_Clinica/web_urls.py

from django.urls import path
from . import web_views # Importamos el nuevo archivo de vistas

urlpatterns = [
    path('especialidades/', web_views.especialidad_list_create_view, name='especialidades_html'),
    path('medicos/', web_views.medico_list_create_view, name='medicos_html'),
    path('pacientes/', web_views.paciente_list_create_view, name='pacientes_html'),
    path('consultas/', web_views.consulta_list_create_view, name='consultas_html'),
    path('tratamientos/', web_views.tratamiento_list_create_view, name='tratamientos_html'),
    path('medicamentos/', web_views.medicamento_list_create_view, name='medicamentos_html'),
    path('recetas/', web_views.receta_list_create_view, name='recetas_html'),
]