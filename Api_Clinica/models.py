from django.db import models

# Choices para Tipo de Sangre
TIPO_SANGRE_CHOICES = [
    ('A+', 'A Positivo'),
    ('A-', 'A Negativo'),
    ('B+', 'B Positivo'),
    ('B-', 'B Negativo'),
    ('AB+', 'AB Positivo'),
    ('AB-', 'AB Negativo'),
    ('O+', 'O Positivo'),
    ('O-', 'O Negativo'),
]

# Choices para Estado de Consulta
ESTADO_CONSULTA_CHOICES = [
    ('PENDIENTE', 'Pendiente'),
    ('COMPLETADA', 'Completada'),
    ('CANCELADA', 'Cancelada'),
]


class Especialidad(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Especialidad"
        verbose_name_plural = "Especialidades"
        ordering = ['nombre']


class Medico(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    rut = models.CharField(max_length=12, unique=True)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    activo = models.BooleanField(default=True)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE, related_name='medicos')

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.especialidad.nombre})"
    
    def get_full_name(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name = "Médico"
        verbose_name_plural = "Médicos"
        ordering = ['apellido', 'nombre']


class Paciente(models.Model):
    id = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    tipo_sangre = models.CharField(max_length=3, choices=TIPO_SANGRE_CHOICES)
    correo = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rut})"
    
    def get_full_name(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ['apellido', 'nombre']


class ConsultaMedica(models.Model):
    id = models.AutoField(primary_key=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='consultas')
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='consultas_atendidas')
    fecha_consulta = models.DateTimeField()
    motivo = models.TextField()
    diagnostico = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CONSULTA_CHOICES, default='PENDIENTE')

    def __str__(self):
        return f"Consulta de {self.paciente} con {self.medico} el {self.fecha_consulta.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = "Consulta Médica"
        verbose_name_plural = "Consultas Médicas"
        ordering = ['-fecha_consulta']


class Tratamiento(models.Model):
    id = models.AutoField(primary_key=True)
    consulta = models.ForeignKey(ConsultaMedica, on_delete=models.CASCADE, related_name='tratamientos')
    descripcion = models.TextField()
    duracion_dias = models.IntegerField()
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Tratamiento para consulta {self.consulta.id}: {self.descripcion[:50]}..."

    class Meta:
        verbose_name = "Tratamiento"
        verbose_name_plural = "Tratamientos"
        ordering = ['-id']


class Medicamento(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    laboratorio = models.CharField(max_length=100)
    stock = models.IntegerField(default=0)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nombre} ({self.laboratorio})"

    class Meta:
        verbose_name = "Medicamento"
        verbose_name_plural = "Medicamentos"
        ordering = ['nombre']


class RecetaMedica(models.Model):
    id = models.AutoField(primary_key=True)
    tratamiento = models.ForeignKey(Tratamiento, on_delete=models.CASCADE, related_name='recetas')
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE, related_name='recetas_asociadas')
    dosis = models.CharField(max_length=100)
    frecuencia = models.CharField(max_length=100)
    duracion = models.CharField(max_length=100) # Podría ser un IntegerField si siempre son días, o CharField para mayor flexibilidad (ej: "7 días", "hasta terminar")

    def __str__(self):
        return f"Receta para {self.medicamento.nombre} en tratamiento {self.tratamiento.id}"

    class Meta:
        verbose_name = "Receta Médica"
        verbose_name_plural = "Recetas Médicas"
        ordering = ['-id']
        
class ReporteLaboratorio(models.Model):
    id = models.AutoField(primary_key=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='reportes_laboratorio')
    # Relación a la consulta que solicitó el reporte
    consulta_origen = models.ForeignKey(ConsultaMedica, on_delete=models.SET_NULL, null=True, blank=True, related_name='reportes_laboratorio_solicitados')
    tipo_examen = models.CharField(max_length=150) # Ej: "Hemograma completo", "Perfil lipídico", "Examen de orina"
    fecha_solicitud = models.DateField(auto_now_add=True)
    fecha_resultado = models.DateField(null=True, blank=True)
    resultados = models.TextField() # Aquí se podría almacenar el texto del resultado o un enlace a un documento
    analizado_por = models.CharField(max_length=100, blank=True, null=True) # Ej: Nombre del técnico o laboratorio

    def __str__(self):
        return f"Reporte de {self.tipo_examen} para {self.paciente.get_full_name()} (Solicitud: {self.fecha_solicitud})"

    class Meta:
        verbose_name = "Reporte de Laboratorio"
        verbose_name_plural = "Reportes de Laboratorio"
        ordering = ['-fecha_solicitud']