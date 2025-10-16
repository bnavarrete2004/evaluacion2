import os
import django
from django.core.management.base import BaseCommand
from datetime import date, datetime, timedelta
import random
from faker import Faker

# NOTA: Ya no necesitamos os.environ.setdefault ni django.setup()
# Django se encarga de eso cuando se ejecuta como un comando de manage.py

from Api_Clinica.models import (
    Especialidad,
    Medico,
    Paciente,
    ConsultaMedica,
    Tratamiento,
    Medicamento,
    RecetaMedica,
    TIPO_SANGRE_CHOICES,
    ESTADO_CONSULTA_CHOICES
)

fake = Faker('es_CL') # 'es_CL' para datos chilenos (RUTs, nombres, etc.)

def generate_rut():
    """Genera un RUT chileno válido (sin puntos ni guion) con dígito verificador."""
    # Genera 7 u 8 dígitos aleatorios
    digits = random.randint(1_000_000, 25_000_000)
    
    # Calcula el dígito verificador
    s = str(digits)
    reversed_digits = [int(d) for d in s[::-1]]
    factor = 2
    sum_ = 0
    for d in reversed_digits:
        sum_ += d * factor
        factor += 1
        if factor > 7:
            factor = 2
    
    remainder = sum_ % 11
    dv = 11 - remainder
    if dv == 10:
        dv = 'K'
    elif dv == 11:
        dv = '0'
    else:
        dv = str(dv)
    
    return f"{digits}-{dv}"


class Command(BaseCommand):
    help = 'Seeds the database with realistic test data for the clinic system.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Iniciando la generación de datos de prueba..."))

        # Limpiar datos existentes (opcional, cuidado en producción)
        self.stdout.write("Limpiando datos existentes (RecetaMedica, Medicamento, Tratamiento, ConsultaMedica, Paciente, Medico, Especialidad)...")
        # Es mejor borrar en orden inverso a la creación para evitar problemas de Foreign Key
        RecetaMedica.objects.all().delete()
        Medicamento.objects.all().delete()
        Tratamiento.objects.all().delete()
        ConsultaMedica.objects.all().delete()
        Paciente.objects.all().delete()
        Medico.objects.all().delete()
        Especialidad.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Datos anteriores eliminados."))

        # 1. Especialidades
        especialidades_data = [
            "Cardiología", "Dermatología", "Pediatría", "Medicina General",
            "Ginecología", "Oftalmología", "Neurología", "Traumatología",
            "Endocrinología", "Urología", "Psicología", "Nutrición"
        ]
        especialidades_objs = []
        self.stdout.write("Creando especialidades...")
        for esp_nombre in especialidades_data:
            try:
                especialidades_objs.append(Especialidad.objects.create(
                    nombre=esp_nombre,
                    descripcion=fake.sentence(nb_words=10)
                ))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creando especialidad '{esp_nombre}': {e}"))
        self.stdout.write(self.style.SUCCESS(f"Creadas {len(especialidades_objs)} especialidades."))

        # 2. Médicos
        medicos_objs = []
        if not especialidades_objs:
            self.stdout.write(self.style.WARNING("No hay especialidades, no se pueden crear médicos."))
        else:
            self.stdout.write("Creando médicos...")
            for _ in range(20): # 20 médicos
                try:
                    medicos_objs.append(Medico.objects.create(
                        nombre=fake.first_name(),
                        apellido=fake.last_name(),
                        rut=generate_rut(),
                        correo=fake.unique.email(),
                        telefono=fake.phone_number(),
                        activo=fake.boolean(chance_of_getting_true=90), # 90% activos
                        especialidad=random.choice(especialidades_objs)
                    ))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error creando médico: {e}"))
            self.stdout.write(self.style.SUCCESS(f"Creados {len(medicos_objs)} médicos."))

        # 3. Pacientes
        pacientes_objs = []
        self.stdout.write("Creando pacientes...")
        for _ in range(50): # 50 pacientes
            try:
                birth_date = fake.date_of_birth(minimum_age=1, maximum_age=90)
                pacientes_objs.append(Paciente.objects.create(
                    rut=generate_rut(),
                    nombre=fake.first_name(),
                    apellido=fake.last_name(),
                    fecha_nacimiento=birth_date,
                    tipo_sangre=random.choice([choice[0] for choice in TIPO_SANGRE_CHOICES]),
                    correo=fake.unique.email(),
                    telefono=fake.phone_number(),
                    direccion=fake.address(),
                    activo=fake.boolean(chance_of_getting_true=95) # 95% activos
                ))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creando paciente: {e}"))
        self.stdout.write(self.style.SUCCESS(f"Creados {len(pacientes_objs)} pacientes."))

        # 4. Medicamentos
        medicamentos_data = [
            ("Paracetamol", "Laboratorio Chile", 100, 3500.00),
            ("Ibuprofeno", "Recalcine", 75, 5200.50),
            ("Amoxicilina", "Savai", 50, 8900.00),
            ("Losartán", "Andrómaco", 60, 12500.75),
            ("Omeprazol", "Farpasa", 90, 7100.00),
            ("Atorvastatina", "Pfizer", 40, 15000.00),
            ("Metformina", "Novartis", 80, 9800.00),
            ("Salbutamol", "GSK", 30, 6000.00),
            ("Dexametasona", "Merck", 25, 4500.00),
            ("Clonazepam", "Sanofi", 120, 11000.00),
        ]
        medicamentos_objs = []
        self.stdout.write("Creando medicamentos...")
        for nombre, lab, stock, precio in medicamentos_data:
            try:
                medicamentos_objs.append(Medicamento.objects.create(
                    nombre=nombre,
                    laboratorio=lab,
                    stock=stock,
                    precio_unitario=precio
                ))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creando medicamento '{nombre}': {e}"))
        self.stdout.write(self.style.SUCCESS(f"Creados {len(medicamentos_objs)} medicamentos."))

        # 5. Consultas Médicas
        consultas_objs = []
        if not pacientes_objs or not medicos_objs:
            self.stdout.write(self.style.WARNING("No hay pacientes o médicos, no se pueden crear consultas médicas."))
        else:
            self.stdout.write("Creando consultas médicas...")
            for i in range(100): # 100 consultas
                try:
                    fecha_consulta = fake.date_time_between(start_date='-2y', end_date='+60d') 
                    
                    estado = None # Inicializamos a None
                    if fecha_consulta > datetime.now(): # Es una consulta futura
                        estado = 'PENDIENTE' 
                    else: # Es una consulta pasada o actual
                        estado = random.choice(['COMPLETADA', 'CANCELADA'])
                    
                    diagnostico_generado = None
                    if estado == 'COMPLETADA':
                        diagnostico_generado = fake.paragraph(nb_sentences=2)
                        
                    consulta = ConsultaMedica.objects.create(
                        paciente=random.choice(pacientes_objs),
                        medico=random.choice(medicos_objs),
                        fecha_consulta=fecha_consulta,
                        motivo=fake.sentence(nb_words=15),
                        diagnostico=diagnostico_generado,
                        estado=estado
                    )
                    consultas_objs.append(consulta)
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error creando consulta médica {i+1}: {e}"))
            self.stdout.write(self.style.SUCCESS(f"Creadas {len(consultas_objs)} consultas médicas."))

        # 6. Tratamientos (solo para consultas completadas)
        tratamientos_objs = []
        self.stdout.write("Iniciando creación de tratamientos...")
        
        consultas_completadas_con_diagnostico = [c for c in consultas_objs if c.estado == 'COMPLETADA' and c.diagnostico]
        self.stdout.write(f"  -> {len(consultas_completadas_con_diagnostico)} consultas 'COMPLETADA' y con diagnóstico encontradas para tratamientos.")

        if not consultas_completadas_con_diagnostico:
            self.stdout.write(self.style.WARNING("No hay consultas médicas completadas con diagnóstico, no se pueden crear tratamientos."))
        else:
            self.stdout.write("Creando tratamientos...")
            for consulta in consultas_completadas_con_diagnostico:
                if fake.boolean(chance_of_getting_true=70): # 70% de las consultas completadas tienen tratamiento
                    try:
                        tratamientos_objs.append(Tratamiento.objects.create(
                            consulta=consulta,
                            descripcion=fake.paragraph(nb_sentences=3),
                            duracion_dias=random.randint(7, 90),
                            observaciones=fake.sentence(nb_words=10) if fake.boolean(chance_of_getting_true=50) else None
                        ))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error al crear tratamiento para consulta ID {consulta.id}: {e}"))
            self.stdout.write(self.style.SUCCESS(f"Creados {len(tratamientos_objs)} tratamientos."))

        # 7. Recetas Médicas (para tratamientos existentes)
        recetas_objs = []
        self.stdout.write("Iniciando creación de recetas médicas...")
        
        if not tratamientos_objs:
            self.stdout.write(self.style.WARNING("No hay tratamientos, no se pueden crear recetas médicas."))
        elif not medicamentos_objs:
            self.stdout.write(self.style.WARNING("No hay medicamentos, no se pueden crear recetas médicas."))
        else:
            self.stdout.write("Creando recetas médicas...")
            for tratamiento in tratamientos_objs:
                num_medicamentos = random.randint(1, min(3, len(medicamentos_objs))) # Entre 1 y 3 medicamentos por tratamiento, o menos si no hay tantos
                meds_for_tratamiento = random.sample(medicamentos_objs, num_medicamentos)
                for med in meds_for_tratamiento:
                    try:
                        recetas_objs.append(RecetaMedica.objects.create(
                            tratamiento=tratamiento,
                            medicamento=med,
                            dosis=f"{random.randint(1, 2)} {random.choice(['comprimidos', 'gotas', 'ml', 'inhalaciones'])}", # Simplificado el if para Salbutamol
                            frecuencia=f"cada {random.choice([6, 8, 12, 24])} horas",
                            duracion=f"{random.randint(5, 30)} días"
                        ))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error al crear receta para tratamiento ID {tratamiento.id}, medicamento '{med.nombre}': {e}"))
            self.stdout.write(self.style.SUCCESS(f"Creadas {len(recetas_objs)} recetas médicas."))

        self.stdout.write(self.style.SUCCESS("\n¡Generación de datos de prueba finalizada con éxito!"))
        self.stdout.write(self.style.SUCCESS("Puedes acceder a ellos a través del admin de Django o tu API."))