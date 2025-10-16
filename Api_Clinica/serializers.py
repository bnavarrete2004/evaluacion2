from rest_framework import serializers
from .models import (
    Especialidad,
    Medico,
    Paciente,
    ConsultaMedica,
    Tratamiento,
    Medicamento,
    RecetaMedica,
    ReporteLaboratorio
)

# Serializer para Especialidad
class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidad
        fields = '__all__' # Incluye todos los campos del modelo

# Serializer para Medico
class MedicoSerializer(serializers.ModelSerializer):
    especialidad_nombre = serializers.ReadOnlyField(source='especialidad.nombre') # Muestra el nombre de la especialidad

    class Meta:
        model = Medico
        fields = [
            'id', 'nombre', 'apellido', 'rut', 'correo',
            'telefono', 'activo', 'especialidad', 'especialidad_nombre'
        ]
        read_only_fields = ['especialidad_nombre'] # Este campo es solo de lectura

# Serializer para Paciente
class PacienteSerializer(serializers.ModelSerializer):
    tipo_sangre_display = serializers.CharField(source='get_tipo_sangre_display', read_only=True) # Muestra el display del choice

    class Meta:
        model = Paciente
        fields = '__all__'

# Serializer para Medicamento
class MedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicamento
        fields = '__all__'

# Serializer para RecetaMedica (Detallado para mostrar información del medicamento)
class RecetaMedicaSerializer(serializers.ModelSerializer):
    medicamento_info = MedicamentoSerializer(source='medicamento', read_only=True) # Anida el serializer de Medicamento

    class Meta:
        model = RecetaMedica
        fields = [
            'id', 'tratamiento', 'medicamento', 'medicamento_info',
            'dosis', 'frecuencia', 'duracion'
        ]
        read_only_fields = ['medicamento_info']


# Serializer para Tratamiento (con recetas anidadas)
class TratamientoSerializer(serializers.ModelSerializer):
    recetas = RecetaMedicaSerializer(many=True, read_only=True) # Anida las recetas asociadas

    class Meta:
        model = Tratamiento
        fields = [
            'id', 'consulta', 'descripcion', 'duracion_dias',
            'observaciones', 'recetas'
        ]


# Serializer para ConsultaMedica (con profundidad para ver médico y paciente, y tratamientos)
class ConsultaMedicaSerializer(serializers.ModelSerializer):
    paciente_nombre_completo = serializers.ReadOnlyField(source='paciente.get_full_name') # Asumiendo un método get_full_name en Paciente
    medico_nombre_completo = serializers.ReadOnlyField(source='medico.get_full_name') # Asumiendo un método get_full_name en Medico
    especialidad_medico = serializers.ReadOnlyField(source='medico.especialidad.nombre')
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    tratamientos = TratamientoSerializer(many=True, read_only=True) # Anida los tratamientos asociados

    class Meta:
        model = ConsultaMedica
        fields = [
            'id', 'paciente', 'paciente_nombre_completo', 'medico', 'medico_nombre_completo',
            'especialidad_medico', 'fecha_consulta', 'motivo', 'diagnostico', 'estado',
            'estado_display', 'tratamientos'
        ]
        read_only_fields = [
            'paciente_nombre_completo', 'medico_nombre_completo',
            'especialidad_medico', 'estado_display'
        ]

    # Para los campos paciente_nombre_completo y medico_nombre_completo,
    # necesitarías añadir estos métodos a los modelos Paciente y Medico
    # en models.py si quieres usarlos:
    #
    # En Paciente:
    # def get_full_name(self):
    #     return f"{self.nombre} {self.apellido}"
    #
    # En Medico:
    # def get_full_name(self):
    #     return f"{self.nombre} {self.apellido}"
    
    
# Serializer para ReporteLaboratorio
class ReporteLaboratorioSerializer(serializers.ModelSerializer):
    # Campo de solo lectura para mostrar el nombre completo del paciente
    paciente_nombre_completo = serializers.ReadOnlyField(source='paciente.get_full_name')

    # Campo de solo lectura para mostrar la fecha de la consulta de origen
    # Usamos CharField para un formato legible, o DateTimeField si la consulta_origen.fecha_consulta es un DateTime
    consulta_origen_fecha = serializers.DateTimeField(source='consulta_origen.fecha_consulta', read_only=True, format="%Y-%m-%d %H:%M")
    
    # Campo de solo lectura para mostrar el motivo de la consulta de origen
    consulta_origen_motivo = serializers.ReadOnlyField(source='consulta_origen.motivo')

    class Meta:
        model = ReporteLaboratorio
        fields = [
            'id',
            'paciente', # ID del paciente
            'paciente_nombre_completo', # Nombre legible del paciente
            'consulta_origen', # ID de la consulta que originó el reporte (puede ser null)
            'consulta_origen_fecha', # Fecha legible de la consulta de origen
            'consulta_origen_motivo', # Motivo legible de la consulta de origen
            'tipo_examen',
            'fecha_solicitud',
            'fecha_resultado',
            'resultados',
            'analizado_por',
        ]
        read_only_fields = [
            'paciente_nombre_completo',
            'consulta_origen_fecha',
            'consulta_origen_motivo',
            'fecha_solicitud', # Generalmente, la fecha de solicitud se establece automáticamente
        ]