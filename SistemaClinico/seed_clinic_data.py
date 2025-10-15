import os
import django
from datetime import date, datetime, timedelta
import random
from faker import Faker

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SistemaClinico.settings') 
django.setup()

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


def seed_data():
    print("Iniciando la generación de datos de prueba...")

    # Limpiar datos existentes (opcional, cuidado en producción)
    print("Limpiando datos existentes (Especialidad, Medico, Paciente, etc.)...")
    RecetaMedica.objects.all().delete()
    Medicamento.objects.all().delete()
    Tratamiento.objects.all().delete()
    ConsultaMedica.objects.all().delete()
    Paciente.objects.all().delete()
    Medico.objects.all().delete()
    Especialidad.objects.all().delete()
    print("Datos anteriores eliminados.")

    # 1. Especialidades
    especialidades_data = [
        "Cardiología", "Dermatología", "Pediatría", "Medicina General",
        "Ginecología", "Oftalmología", "Neurología", "Traumatología",
        "Endocrinología", "Urología", "Psicología", "Nutrición"
    ]
    especialidades_objs = []
    print("Creando especialidades...")
    for esp_nombre in especialidades_data:
        especialidades_objs.append(Especialidad.objects.create(
            nombre=esp_nombre,
            descripcion=fake.sentence(nb_words=10)
        ))
    print(f"Creadas {len(especialidades_objs)} especialidades.")

    # 2. Médicos
    medicos_objs = []
    print("Creando médicos...")
    for _ in range(20): # 20 médicos
        medicos_objs.append(Medico.objects.create(
            nombre=fake.first_name(),
            apellido=fake.last_name(),
            rut=generate_rut(),
            correo=fake.unique.email(),
            telefono=fake.phone_number(),
            activo=fake.boolean(chance_of_getting_true=90), # 90% activos
            especialidad=random.choice(especialidades_objs)
        ))
    print(f"Creados {len(medicos_objs)} médicos.")

    # 3. Pacientes
    pacientes_objs = []
    print("Creando pacientes...")
    for _ in range(50): # 50 pacientes
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
    print(f"Creados {len(pacientes_objs)} pacientes.")

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
    print("Creando medicamentos...")
    for nombre, lab, stock, precio in medicamentos_data:
        medicamentos_objs.append(Medicamento.objects.create(
            nombre=nombre,
            laboratorio=lab,
            stock=stock,
            precio_unitario=precio
        ))
    print(f"Creados {len(medicamentos_objs)} medicamentos.")

    # 5. Consultas Médicas
    consultas_objs = []
    print("Creando consultas médicas...")
    for _ in range(100): # 100 consultas
        # Generar fecha de consulta en los últimos 2 años o futuro cercano
        fecha_consulta = fake.date_time_between(start_date='-2y', end_date='+60d') 
        estado = random.choice([choice[0] for choice in ESTADO_CONSULTA_CHOICES])
        
        # Si la consulta es futura, es probable que esté pendiente
        if fecha_consulta > datetime.now() and estado != 'PENDIENTE':
            estado = 'PENDIENTE'
        # Si la consulta es pasada, es probable que esté completada o cancelada
        elif fecha_consulta < datetime.now() and estado == 'PENDIENTE':
             estado = random.choice(['COMPLETADA', 'CANCELADA'])


        consulta = ConsultaMedica.objects.create(
            paciente=random.choice(pacientes_objs),
            medico=random.choice(medicos_objs),
            fecha_consulta=fecha_consulta,
            motivo=fake.sentence(nb_words=15),
            diagnostico=fake.paragraph(nb_sentences=2) if estado == 'COMPLETADA' else None, # Solo hay diagnóstico si está completada
            estado=estado
        )
        consultas_objs.append(consulta)
    print(f"Creadas {len(consultas_objs)} consultas médicas.")

    # 6. Tratamientos (solo para consultas completadas)
    tratamientos_objs = []
    print("Creando tratamientos...")
    for consulta in consultas_objs:
        if consulta.estado == 'COMPLETADA' and fake.boolean(chance_of_getting_true=70): # 70% de las consultas completadas tienen tratamiento
            tratamientos_objs.append(Tratamiento.objects.create(
                consulta=consulta,
                descripcion=fake.paragraph(nb_sentences=3),
                duracion_dias=random.randint(7, 90),
                observaciones=fake.sentence(nb_words=10) if fake.boolean(chance_of_getting_true=50) else None
            ))
    print(f"Creados {len(tratamientos_objs)} tratamientos.")

    # 7. Recetas Médicas (para tratamientos existentes)
    recetas_objs = []
    print("Creando recetas médicas...")
    for tratamiento in tratamientos_objs:
        num_medicamentos = random.randint(1, 3) # Entre 1 y 3 medicamentos por tratamiento
        meds_for_tratamiento = random.sample(medicamentos_objs, min(num_medicamentos, len(medicamentos_objs)))
        for med in meds_for_tratamiento:
            recetas_objs.append(RecetaMedica.objects.create(
                tratamiento=tratamiento,
                medicamento=med,
                dosis=f"{random.randint(1, 2)} {random.choice(['comprimidos', 'gotas', 'ml']) if med.nombre != 'Salbutamol' else 'inhalaciones'} ",
                frecuencia=f"cada {random.choice([6, 8, 12, 24])} horas",
                duracion=f"{random.randint(5, 30)} días"
            ))
    print(f"Creadas {len(recetas_objs)} recetas médicas.")

    print("\n¡Generación de datos de prueba finalizada con éxito!")
    print("Puedes acceder a ellos a través del admin de Django o tu API.")


if __name__ == '__main__':
    seed_data()