from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    Especialidad,
    Medico,
    Paciente,
    ConsultaMedica,
    Tratamiento,
    Medicamento,
    RecetaMedica,
    ReporteLaboratorio # ¡Importa tu nuevo modelo aquí!
)
from .serializers import (
    EspecialidadSerializer,
    MedicoSerializer,
    PacienteSerializer,
    ConsultaMedicaSerializer,
    TratamientoSerializer,
    MedicamentoSerializer,
    RecetaMedicaSerializer,
    ReporteLaboratorioSerializer # ¡Importa tu nuevo serializador aquí!
)

# Puedes personalizar los permisos por ViewSet.
# Por simplicidad, aquí usamos AllowAny para todos,
# pero en un entorno real querrías más seguridad.

class EspecialidadViewSet(viewsets.ModelViewSet):
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer
    permission_classes = [AllowAny] # Permite acceso a cualquiera
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nombre', 'descripcion'] # Permite buscar por nombre y descripción
    ordering_fields = ['nombre', 'id'] # Permite ordenar por nombre y id

class MedicoViewSet(viewsets.ModelViewSet):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['especialidad', 'activo'] # Permite filtrar por ID de especialidad y estado activo
    search_fields = ['nombre', 'apellido', 'rut', 'correo']
    ordering_fields = ['apellido', 'nombre', 'especialidad__nombre']

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['activo', 'tipo_sangre'] # Permite filtrar por estado activo y tipo de sangre
    search_fields = ['nombre', 'apellido', 'rut', 'correo', 'telefono']
    ordering_fields = ['apellido', 'nombre', 'fecha_nacimiento']

class ConsultaMedicaViewSet(viewsets.ModelViewSet):
    queryset = ConsultaMedica.objects.all()
    serializer_class = ConsultaMedicaSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['paciente', 'medico', 'estado', 'fecha_consulta'] # Filtra por paciente, médico, estado y fecha
    search_fields = ['motivo', 'diagnostico', 'paciente__nombre', 'medico__apellido'] # Busca en motivo, diagnóstico, nombre de paciente, apellido de médico
    ordering_fields = ['fecha_consulta', 'estado']

class TratamientoViewSet(viewsets.ModelViewSet):
    queryset = Tratamiento.objects.all()
    serializer_class = TratamientoSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['consulta', 'duracion_dias'] # Filtra por ID de consulta y duración
    search_fields = ['descripcion', 'observaciones']
    ordering_fields = ['duracion_dias', 'id']

class MedicamentoViewSet(viewsets.ModelViewSet):
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nombre', 'laboratorio']
    ordering_fields = ['nombre', 'laboratorio', 'stock', 'precio_unitario']

class RecetaMedicaViewSet(viewsets.ModelViewSet):
    queryset = RecetaMedica.objects.all()
    serializer_class = RecetaMedicaSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['tratamiento', 'medicamento'] # Filtra por ID de tratamiento y medicamento
    search_fields = ['dosis', 'frecuencia', 'duracion']
    ordering_fields = ['id', 'tratamiento__id', 'medicamento__nombre']

# ¡Aquí va el nuevo ViewSet para ReporteLaboratorio!
class ReporteLaboratorioViewSet(viewsets.ModelViewSet):
    queryset = ReporteLaboratorio.objects.all()
    serializer_class = ReporteLaboratorioSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # Puedes filtrar por paciente, consulta_origen o tipo de examen
    filterset_fields = ['paciente', 'consulta_origen', 'tipo_examen', 'fecha_solicitud', 'fecha_resultado']
    # Puedes buscar en el tipo de examen, los resultados, el nombre del paciente o el motivo de la consulta de origen
    search_fields = [
        'tipo_examen',
        'resultados',
        'analizado_por',
        'paciente__nombre',
        'paciente__apellido',
        'consulta_origen__motivo'
    ]
    # Permite ordenar por fecha de solicitud, fecha de resultado, tipo de examen o nombre del paciente
    ordering_fields = [
        'fecha_solicitud',
        'fecha_resultado',
        'tipo_examen',
        'paciente__apellido',
        'paciente__nombre'
    ]