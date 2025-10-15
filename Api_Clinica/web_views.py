# Api_Clinica/web_views.py

from django.shortcuts import render

# Función para la vista de Especialidades (CRUD con HTML/JS)
def especialidad_list_create_view(request):
    """
    Renderiza la plantilla para gestionar especialidades.
    La lógica de CRUD se manejará en el frontend con JavaScript
    interactuando con la API REST.
    """
    return render(request, 'api_clinica/especialidades.html', {'title': 'Gestión de Especialidades'})

# Función para la vista de Médicos (CRUD con HTML/JS)
def medico_list_create_view(request):
    """
    Renderiza la plantilla para gestionar médicos.
    """
    return render(request, 'api_clinica/medicos.html', {'title': 'Gestión de Médicos'})

# Función para la vista de Pacientes (CRUD con HTML/JS)
def paciente_list_create_view(request):
    """
    Renderiza la plantilla para gestionar pacientes.
    """
    return render(request, 'api_clinica/pacientes.html', {'title': 'Gestión de Pacientes'})

# Función para la vista de Consultas Médicas (CRUD con HTML/JS)
def consulta_list_create_view(request):
    """
    Renderiza la plantilla para gestionar consultas médicas.
    """
    return render(request, 'api_clinica/consultas.html', {'title': 'Gestión de Consultas Médicas'})

# Función para la vista de Tratamientos (CRUD con HTML/JS)
def tratamiento_list_create_view(request):
    """
    Renderiza la plantilla para gestionar tratamientos.
    """
    return render(request, 'api_clinica/tratamientos.html', {'title': 'Gestión de Tratamientos'})

# Función para la vista de Medicamentos (CRUD con HTML/JS)
def medicamento_list_create_view(request):
    """
    Renderiza la plantilla para gestionar medicamentos.
    """
    return render(request, 'api_clinica/medicamentos.html', {'title': 'Gestión de Medicamentos'})

# Función para la vista de Recetas Médicas (CRUD con HTML/JS)
def receta_list_create_view(request):
    """
    Renderiza la plantilla para gestionar recetas médicas.
    """
    return render(request, 'api_clinica/recetas.html', {'title': 'Gestión de Recetas Médicas'})