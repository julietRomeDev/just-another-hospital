#Author: Amanda Julieta
#Version: 1.1
#Date: 2026-08-14 America/South_America/Argentina


import mysql.connector
from faker import Faker
import random
from datetime import datetime, timedelta


print("==== Fase 1: Generar Usuarios...")
print("==== JustAnother Hospital === - Fake Users Config...")
fake = Faker('es_AR')

# Establecer conexión
try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password=''
    )
    cursor = conn.cursor(dictionary=True)
    print("[*] Conexion establecida exitosamente...")
except mysql.connector.Error as err:
    print(f"[!] Error al conectar a la base de datos: {err}")
    exit(1)

# Validación de conexión
try:
    cursor.execute("SELECT VERSION();")
    version = cursor.fetchone()
    print(f"[*] Base de datos conectada correctamente: Current Version: {version[0]}")
except Exception as e:
    print(f"[!] Error al validar la conexion: {e}")

# Seleccionar la base de datos
cursor.execute("USE db_justanother_hospital")
print("[*] Generando usuarios... ")
print("")

# 1. Insertar el elenco estelar fijo (Los personajes icónicos)
empleados_fijos = [
    ("Gregory", "House", "gregory.house", "gregory.house@justanotherhospital.domain", "everybodylies", "medico"),
    ("Lisa", "Cuddy", "lisa.cuddy", "lisa.cuddy@justanotherhospital.domain", "housedoeseverythingwrong", "administrativo"),
    ("James", "Wilson", "dr.wilson", "dr.wilson@justanotherhospital.domain", "housenotagain", "medico"),
    ("Soy", "Una Arveja", "soyunarvena", "soyunarvena@elcuartetodenos.com", "elcuartetodenos", "administrativo"),
    ("Paciente", "Lupus", "holalupus", "holatengoluppus@llamenahouse.com", "eslupus", "medico"),
    ("Wilson", "Spoiler", "wilsondie", "wilsondieinthefinalseason@idonwannaspoiltheparty.com", "nopoil", "medico")
]

print("[*] Insertando personal icónico de JustAnother Hospital...")
for emp in empleados_fijos:
    nombre, apellido, nombre_usuario, email, password, rol = emp
    cursor.execute(
        "INSERT INTO usuarios (nombre, apellido, nombre_usuario, email, password, rol) VALUES (%s, %s, %s, %s, %s, %s)",
        (nombre, apellido, nombre_usuario, email, password, rol)
    )
    print(f" - Nombre: {nombre} {apellido} | Usuario: {nombre_usuario} | Rol: {rol} | Email: {email} | Password: {password}")

print("")

# 2. Generar usuarios aleatorios por rol usando Faker
roles = ['medico', 'enfermero', 'farmaceutico', 'administrativo']

for rol in roles:
    print(f"[*] Generando seis {rol}es adicionales...")

    for _ in range(6):
        nombre = fake.first_name()
        apellido = fake.last_name()
        nombre_usuario = fake.user_name()
        password = fake.password(length=10)
        email = fake.ascii_free_email()

        cursor.execute(
            "INSERT INTO usuarios (nombre, apellido, nombre_usuario, email, password, rol) VALUES (%s, %s, %s, %s, %s, %s)",
            (nombre, apellido, nombre_usuario, email, password, rol)
        )
        
        print(f" - Nombre: {nombre} | Apellido: {apellido}")
        print(f"    - Usuario: {nombre_usuario} | Rol: {rol} | Email: {email} | Password: {password}")

print("==== Fase 1: Generar Usuarios Completada ====")
print("==== Comenzando Fase 2: Estructura Fisica")
print("\n[*] Generando Pisos del Edificio...")
pisos = ["Planta Baja", "Piso 1", "Piso 2", "Piso 3", "Subsuelo"]
piso_ids = []

for nombre_piso in pisos:
    cursor.execute(
        "INSERT INTO pisos_edificio (nombre) VALUES (%s)",
        (nombre_piso,)
    )
    piso_ids.append(cursor.lastrowid)
    print(f" - Creado Piso: {nombre_piso}")

# ---------------------------------------------------------
# 3. SECTORES
# ---------------------------------------------------------
print("\n[*] Generando Sectores del Hospital...")
sectores_data = [
    ("Guardia y Emergencias", piso_ids[0]),
    ("Farmacia Central", piso_ids[0]),
    ("Consultorios Externos", piso_ids[1]),
    ("Internación General", piso_ids[2]),
    ("Terapia Intensiva (UTI)", piso_ids[3]),
    ("Quórfanos / Cirugía", piso_ids[3]),
    ("Mantenimiento y Depósito", piso_ids[4])
]
sector_ids = []

for nombre_sec, id_piso in sectores_data:
    cursor.execute(
        "INSERT INTO sectores (nombre, piso_id) VALUES (%s, %s)",
        (nombre_sec, id_piso)
    )
    sector_ids.append(cursor.lastrowid)
    print(f" - Creado Sector: {nombre_sec}")

# ---------------------------------------------------------
# 4. HABITACIONES Y CAMAS
# ---------------------------------------------------------
print("\n[*] Generando Habitaciones y Camas...")
habitacion_ids = []

# Generar 10 habitaciones en sectores de internación/UTI

for i in range(1, 11):
    numero_habitacion = f"HAB-{100 + i}"
    sector_id = random.choice([sector_ids[3], sector_ids[4]]) # Internación o UTI
    
    cursor.execute(
        "INSERT INTO habitaciones (numero_habitacion, sector_id) VALUES (%s, %s)",
        (numero_habitacion, sector_id)
    )
    hab_id = cursor.lastrowid
    habitacion_ids.append(hab_id)
    
    # Cada habitación tiene 2 camas
    for c in range(1, 3):
        codigo_cama = f"CAMA-{100 + i}-{c}"
        cursor.execute(
            "INSERT INTO camas (codigo_cama, habitacion_id, estado) VALUES (%s, %s, %s)",
            (codigo_cama, hab_id, 'libre')
        )

print(f" - Generadas {len(habitacion_ids)} habitaciones con 2 camas cada una.")

# ---------------------------------------------------------
# 5. ESPECIALIDADES
# ---------------------------------------------------------
print("\n[*] Asignando Especialidades a Médicos...")

# Asegúrate de tener una lista o consulta de las especialidades disponibles
cursor.execute("SELECT id FROM especialidades")
especialidades = [row['id'] for row in cursor.fetchall()]

print("\n[*] Asignando Especialidades a Médicos...")

# 1. Obtenemos los IDs de los empleados que son médicos directamente de la base de datos
cursor.execute("SELECT id FROM empleados WHERE tipo_empleado = 'medico'")
empleado_medicos_ids = [row['id'] for row in cursor.fetchall()]

# 2. Obtenemos las especialidades disponibles
cursor.execute("SELECT id FROM especialidades")
especialidades = [row['id'] for row in cursor.fetchall()]

# 3. Asignamos las especialidades
for med_id in empleado_medicos_ids:
    if especialidades:
        esp_asignadas = random.sample(especialidades, min(len(especialidades), random.randint(1, 2)))
        
        for esp_id in esp_asignadas:
            numero_matricula = f"MAT-{random.randint(100000, 999999)}"
            
            cursor.execute("""
                INSERT INTO medicos_especialidades (empleado_id, especialidad_id, numero_matricula) 
                VALUES (%s, %s, %s)
            """, (med_id, esp_id, numero_matricula))

print("[+] Especialidades asignadas correctamente.")

# ---------------------------------------------------------
# 6. EMPLEADOS (Asociando a la tabla 'usuarios' de Fase 1)
# ---------------------------------------------------------
print("\n[*] Vinculando Empleados a los Usuarios...")

# Traemos los usuarios insertados en la Fase 1
cursor.execute("SELECT id_usuario, nombre, apellido, rol FROM usuarios")
usuarios = cursor.fetchall()

empleado_medicos_ids = []
empleado_enfermeros_ids = []

for u in usuarios:
    dni = str(fake.unique.random_number(digits=8, fix_len=True))
    legajo = f"LEG-{random.randint(1000, 9999)}"
    fecha_ingreso = fake.date_between(start_date='-5y', end_date='today')
    
    # Mapeamos el rol del usuario al ENUM de tipo_empleado ('medico', 'enfermero', 'administrativo', 'tecnico')
    tipo_empleado = u['rol'] if u['rol'] in ['medico', 'enfermero', 'administrativo', 'tecnico'] else 'administrativo'

    cursor.execute("""
        INSERT INTO empleados (legajo, dni, nombre, apellido, fecha_ingreso, tipo_empleado) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (legajo, dni, u['nombre'], u['apellido'], fecha_ingreso, tipo_empleado))
    
    emp_id = cursor.lastrowid
    
    if tipo_empleado == 'medico':
        empleado_medicos_ids.append(emp_id)
    elif tipo_empleado == 'enfermero':
        empleado_enfermeros_ids.append(emp_id)

print(f" - Registrados {len(usuarios)} empleados en plantilla.")

# ---------------------------------------------------------
# 7. MEDICOS_ESPECIALIDADES
# ---------------------------------------------------------
print("\n[*] Asignando Especialidades a Médicos...")

# Nos aseguramos de obtener los IDs de las especialidades si no estaban cargados
cursor.execute("SELECT id FROM especialidades")
especialidades = [row['id'] for row in cursor.fetchall()]

# Iteramos sobre los médicos
for med_id in empleado_medicos_ids:
    if especialidades:
        # Usamos 'especialidades' en lugar de 'especialidad_ids'
        esp_asignadas = random.sample(especialidades, min(len(especialidades), random.randint(1, 2)))
        
        for esp_id in esp_asignadas:
            numero_matricula = f"MAT-{random.randint(100000, 999999)}"
            
            cursor.execute("""
                INSERT INTO medicos_especialidades (empleado_id, especialidad_id, numero_matricula) 
                VALUES (%s, %s, %s)
            """, (med_id, esp_id, numero_matricula))

print("[+] Especialidades asignadas correctamente.")

# ---------------------------------------------------------
# 8. HORARIO_PERSONAL
# ---------------------------------------------------------
print("\n[*] Generando Horarios del Personal...")

# Seleccionamos 'id' en lugar de 'id_empleado'
cursor.execute("SELECT id FROM empleados")
empleados = [row['id'] for row in cursor.fetchall()]

dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
turnos = [
    ('08:00:00', '16:00:00', 'Mañana'),
    ('16:00:00', '00:00:00', 'Tarde'),
    ('00:00:00', '08:00:00', 'Noche')
]

for emp_id in empleados:
    # Asignamos de 3 a 5 días de trabajo por empleado
    dias_asignados = random.sample(dias_semana, random.randint(3, 5))
    
    for dia in dias_asignados:
        hora_inicio, hora_fin, turno = random.choice(turnos)
        
        cursor.execute("""
            INSERT INTO horarios_empleados (empleado_id, dia_semana, hora_inicio, hora_fin, turno) 
            VALUES (%s, %s, %s, %s, %s)
        """, (emp_id, dia, hora_inicio, hora_fin, turno))

print("[+] Horarios del personal registrados con éxito.")

# ---------------------------------------------------------
# 9. ENFERMEROS_SECTORES
# ---------------------------------------------------------
print("\n[*] Asignando Enfermeros a Sectores...")

for enf_id in empleado_enfermeros_ids:
    sec_id = random.choice(sector_ids)
    cursor.execute("""
        INSERT INTO enfermeros_sectores (empleado_id, sector_id)
        VALUES (%s, %s)
    """, (enf_id, sec_id))

print("Comenzando Fase 3...")
print("Fase 3: Pacientes")

print("\n[*] Generando Obras Sociales y Prepagas...")

obras_sociales_data = [
    ("OSDE", "30-54678912-3", "Binario 310", "Prepaga"),
    ("Swiss Medical", "30-68934512-4", "SMG 20", "Prepaga"),
    ("Galeno", "30-71234567-9", "Plan 330", "Prepaga"),
    ("Medicus", "30-65432109-8", "Plan Azul", "Prepaga"),
    ("OSECAC", "30-50123456-2", "Plan Estándar", "Obra Social"),
    ("PAMI", "30-54666666-1", "Jubilados y Pensionados", "Obra Social Estatal")
]

obra_social_ids = []

for nombre, cuit, plan, tipo_cobertura in obras_sociales_data:
    cursor.execute("""
        INSERT INTO obras_sociales_prepagas (nombre, cuit, plan, tipo_cobertura) 
        VALUES (%s, %s, %s, %s)
    """, (nombre, cuit, plan, tipo_cobertura))
    
    obra_social_ids.append(cursor.lastrowid)

print(f" - Registradas {len(obra_social_ids)} obras sociales/prepagas.")

# ---------------------------------------------------------
# 10. PACIENTES (Incluyendo al elenco especial de pacientes)
# ---------------------------------------------------------
print("\n[*] Insertando Pacientes (incluyendo casos clínicos especiales)...")

pacientes_fijos = [
    ("Paciente", "Lupus", "40123456", "holatengoluppus@llamenahouse.com", "1155443322", "Calle Falsa 123"),
    ("Paciente", "Spoilers", "41987654", "wilsondieinthefinalseason@idonwannaspoiltheparty.com", "1122334455", "Av. Siempre Viva 742")
]

print("\n[*] Insertando Pacientes...")

paciente_ids = []

for _ in range(15): # O el número de pacientes que estés generando
    nombre = fake.first_name()
    apellido = fake.last_name()
    dni = str(fake.unique.random_number(digits=8, fix_len=True))
    email = fake.email()
    telefono = fake.phone_number()
    direccion = fake.address()
    fecha_nacimiento = fake.date_of_birth(minimum_age=18, maximum_age=90) # Generamos fecha de nacimiento

    cursor.execute("""
        INSERT INTO pacientes (nombre, apellido, dni, email, telefono, direccion, fecha_nacimiento) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (nombre, apellido, dni, email, telefono, direccion, fecha_nacimiento))
    
    paciente_ids.append(cursor.lastrowid)

print(f" - Registrados {len(paciente_ids)} pacientes.")

# ---------------------------------------------------------
# 11. CONTACTOS DE EMERGENCIA
# ---------------------------------------------------------
print("\n[*] Generando Contactos de Emergencia para los pacientes...")

for pac_id in paciente_ids:
    nombre_contacto = fake.name()
    parentesco = random.choice(["Padre", "Madre", "Cónyuge", "Amigo/a", "Hijo/a"])
    telefono_contacto = fake.phone_number()

    cursor.execute("""
        INSERT INTO contactos_emergencia (paciente_id, nombre, parentesco, telefono) 
        VALUES (%s, %s, %s, %s)
    """, (pac_id, nombre_contacto, parentesco, telefono_contacto))

print(" - Contactos de emergencia vinculados.")

# ---------------------------------------------------------
# 12. PACIENTES_COBERTURA (Relación pacientes <-> obras sociales)
# ---------------------------------------------------------
print("\n[*] Asignando Coberturas Médicas a los pacientes...")

for paciente_id in paciente_ids:
    if obra_social_ids:
        # Aquí definiste la variable 'obra_social_id'
        obra_social_id = random.choice(obra_social_ids) 
        numero_afiliado = f"AF-{random.randint(10000000, 99999999)}"
        
        # Corrección: usa la variable 'obra_social_id' que definiste arriba
        cursor.execute("""
            INSERT INTO pacientes_coberturas (paciente_id, cobertura_id, numero_afiliado) 
            VALUES (%s, %s, %s)
        """, (paciente_id, obra_social_id, numero_afiliado))

print("[+] Coberturas médicas asignadas con éxito.")
# ---------------------------------------------------------
# 13. AGENDA_MEDICA (Bloques horarios de los médicos)
# ---------------------------------------------------------
print("\n[*] Generando Agenda Médica para los profesionales...")

# Obtenemos directamente los IDs de la tabla empleados que son médicos
cursor.execute("SELECT id FROM empleados WHERE tipo_empleado = 'medico'")
medicos = [row['id'] for row in cursor.fetchall()]

# Generamos fechas base para simular los bloques horarios (fecha_hora_inicio y fecha_hora_fin)
for med_id in medicos:
    # Creamos algunas agendas aleatorias para los próximos días
    for _ in range(random.randint(2, 3)):
        fecha_inicio = fake.date_time_between(start_date='now', end_date='+10d')
        fecha_fin = fecha_inicio + timedelta(hours=5) # Bloque de 5 horas
        cupo_maximo = random.randint(5, 15)
        
        cursor.execute("""
            INSERT INTO agenda_medica (empleado_id, fecha_hora_inicio, fecha_hora_fin, cupo_maximo) 
            VALUES (%s, %s, %s, %s)
        """, (med_id, fecha_inicio, fecha_fin, cupo_maximo))

print("[+] Agendas médicas generadas exitosamente.")

# ---------------------------------------------------------
# 14. TURNOS
# ---------------------------------------------------------
print("[*] Comenzando Fase 4: Turnos")
print("\n[*] Recuperando pacientes, médicos y agendas existentes...")

# Pacientes (la PK es 'id')
cursor.execute("SELECT id FROM pacientes")
paciente_ids = [row['id'] for row in cursor.fetchall()]

# Médicos (Empleados con tipo_empleado = 'medico')
cursor.execute("SELECT id FROM empleados WHERE tipo_empleado = 'medico'")
medico_ids = [row['id'] for row in cursor.fetchall()]

# Agendas médicas (la PK es 'id')
cursor.execute("SELECT id FROM agenda_medica")
agenda_ids = [row['id'] for row in cursor.fetchall()]

for _ in range(40):
    paciente_id = random.choice(paciente_ids)
    # Nota: si tu tabla turnos relaciona directamente al empleado/medico o mediante agenda, 
    # usa las columnas que definiste en el CREATE TABLE de turnos.
    agenda_id = random.choice(agenda_ids) if agenda_ids else None
    
    fecha_turno = fake.date_time_between(start_date='-30d', end_date='+30d')
    estado = random.choice(['pendiente', 'confirmado', 'cancelado', 'atendido'])

    cursor.execute("""
        INSERT INTO turnos (agenda_id, paciente_id, fecha_hora_turno, estado) 
        VALUES (%s, %s, %s, %s)
    """, (agenda_id, paciente_id, fecha_turno, estado))

# ---------------------------------------------------------
# 15. DIAGNÓSTICOS (Catálogo de enfermedades)
# ---------------------------------------------------------
print("\n[*] Generando Catálogo de Diagnósticos...")

diagnosticos_data = [
    ("Lupus Eritematoso Sistémico", "M32", "Enfermedad autoinmunitaria crónica."),
    ("Infección por parásitos intestinales", "B82", "Causada por carne mal cocida o falta de higiene."),
    ("Vasculitis", "L95", "Inflamación de los vasos sanguíneos."),
    ("Sarcoidosis", "D86", "Crecimiento de células inflamatorias en órganos."),
    ("Intoxicación por metales pesados", "T56", "Presencia de plomo, mercurio u otros metales."),
    ("Amiloidosis", "E85", "Acumulación de proteínas anormales en los órganos."),
    ("Porfiria", "E80", "Trastornos enzimáticos que afectan el sistema nervioso."),
    ("Gripe común", "J11", "Infección viral respiratoria leve.")
]

diagnostico_ids = []

# Ahora desempaquetamos 3 variables: nombre, codigo, descripcion
for nombre, codigo, desc in diagnosticos_data:
    cursor.execute("""
        INSERT INTO Diagnosticos (nombre, codigo_cie10, descripcion_enfermedad) 
        VALUES (%s, %s, %s)
    """, (nombre, codigo, desc)) # Usamos 'codigo' y 'desc' aquí
    
    diagnostico_ids.append(cursor.lastrowid)
    print(f" - Diagnóstico registrado: {nombre} ({codigo})")

diagnostico_ids = []

for nombre, desc in diagnosticos_data:
    cursor.execute("""
        INSERT INTO diagnosticos (nombre, codigo_cie10, descripcion_enfermedad) 
        VALUES (%s, %s, %s)
    """, (nombre, codigo_cie10, descripcion_enfermedad))
    diagnostico_ids.append(cursor.lastrowid)
    print(f" - Diagnóstico registrado: {nombre}")

# ---------------------------------------------------------
# 16. CONSULTAS (Atenciones médicas reales realizadas)
# ---------------------------------------------------------
print("\n[*] Registrando Consultas Médicas y observaciones de diagnóstico...")
consulta_ids = []

# Tomamos algunos turnos que hayan sido 'Atendidos' o simulamos consultas nuevas
cursor.execute("SELECT id_turno, paciente_id, medico_id FROM turnos WHERE estado = 'Atendido'")
turnos_atendidos = cursor.fetchall()

# Si no hay suficientes turnos atendidos, creamos consultas genéricas basadas en pacientes y médicos
for turno in turnos_atendidos[:15]:
    observaciones = fake.text(max_nb_chars=150)
    
    cursor.execute("""
        INSERT INTO consultas (turno_id, paciente_id, medico_id, observaciones, fecha_atencion) 
        VALUES (%s, %s, %s, %s, NOW())
    """, (turno['id_turno'], turno['paciente_id'], turno['medico_id'], observaciones))
    
    consulta_ids.append(cursor.lastrowid)

print(f" - Registradas {len(consulta_ids)} consultas médicas.")

# ---------------------------------------------------------
# 17. CONSULTA_DIAGNOSTICO (Tabla puente)
# ---------------------------------------------------------
print("\n[*] Vinculando Diagnósticos a las Consultas...")

for consulta_id in consulta_ids:
    # Asignamos 1 o 2 diagnósticos por consulta (garantizando que el lupus aparezca muy poco o nada por meme)
    diags_asignados = random.sample(diagnostico_ids, random.randint(1, 2))
    
    for diag_id in diags_asignados:
        cursor.execute("""
            INSERT INTO consulta_diagnostico (consulta_id, diagnostico_id, precision_diagnostica) 
            VALUES (%s, %s, %s)
        """, (consulta_id, diag_id, random.choice(['Preliminar', 'Confirmado', 'Dudoso'])))

print("[+] Diagnosticos Generados Correctamente")
print("[*] Generando Signos Vitales...")
print("[*] Fase 5: Signos Vitales...")

# ---------------------------------------------------------
# 18. RECUPERAR IDS NECESARIOS
# ---------------------------------------------------------
print("\n[*] Recuperando pacientes y consultas existentes...")

cursor.execute("SELECT id_paciente FROM pacientes")
paciente_ids = [row['id_paciente'] for row in cursor.fetchall()]

cursor.execute("SELECT id_consulta, paciente_id, medico_id FROM consultas")
consultas = cursor.fetchall()

# ---------------------------------------------------------
# 19. SIGNOS VITALES
# ---------------------------------------------------------
print("\n[*] Registrando Signos Vitales de los pacientes...")

for pac_id in paciente_ids:
    # Generamos valores médicos realistas (o ligeramente alterados para darle dramatismo)
    presion = f"{random.randint(110, 150)}/{random.randint(70, 95)}"
    temperatura = round(random.uniform(36.0, 39.5), 1)
    frecuencia_cardiaca = random.randint(60, 130)
    saturacion = random.randint(92, 100)
    
    cursor.execute("""
        INSERT INTO signos_vitales (paciente_id, presion_arterial, temperatura, frecuencia_cardiaca, saturacion_oxigeno, fecha_registro) 
        VALUES (%s, %s, %s, %s, %s, NOW())
    """, (pac_id, presion, temperatura, frecuencia_cardiaca, saturacion))

print(f" - Signos vitales registrados para {len(paciente_ids)} pacientes.")

# ---------------------------------------------------------
# 20. TRIAGE Y BOX DE GUARDIA
# ---------------------------------------------------------
print("\n[*] Asignando Triage y Box en la Guardia...")

niveles_triage = ['Rojo (Emergencia)', 'Amarillo (Urgencia)', 'Verde (No urgente)', 'Azul (Consulta menor)']

for i in range(1, 11):
    # Crear un box de guardia simulado
    box_nombre = f"Box de Guardia #{i}"
    paciente_id = random.choice(paciente_ids)
    nivel = random.choice(niveles_triage)
    motivo = fake.sentence(nb_words=6)

    cursor.execute("""
        INSERT INTO triage (paciente_id, nivel_urgencia, motivo_consulta, fecha_hora) 
        VALUES (%s, %s, %s, NOW())
    """, (paciente_id, nivel, motivo))

print(" - Registros de Triage generados.")

# ---------------------------------------------------------
# 21. RECETAS MÉDICAS Y DETALLE DE RECETAS
# ---------------------------------------------------------
print("\n[*] Generando Recetas Médicas y prescripciones...")

# Medicamentos típicos (incluyendo el famoso Vicodin de House)
medicamentos_catalogo = [
    ("Vicodin (Hidrocodona / Paracetamol)", "1 comprimido cada 6 horas ante dolor extremo. (Recetado por House)"),
    ("Ibuprofeno 600mg", "1 comprimido cada 8 horas con alimentos."),
    ("Placebo de azúcar", "1 cada 12 horas para calmar la ansiedad del paciente."),
    ("Metotrexato", "Controlar dosis semanalmente según evolución autoinmune."),
    ("Amoxicilina 1g", "1 comprimido cada 12 horas por 7 días.")
]

for consulta in consultas[:10]: # Creamos recetas para las primeras 10 consultas
    # Crear receta cabecera
    cursor.execute("""
        INSERT INTO recetas_medicas (consulta_id, paciente_id, medico_id, fecha_emision) 
        VALUES (%s, %s, %s, NOW())
    """, (consulta['id_consulta'], consulta['paciente_id'], consulta['medico_id']))
    
    receta_id = cursor.lastrowid
    
    # Agregar entre 1 y 2 medicamentos por receta
    meds_Elegidos = random.sample(medicamentos_catalogo, random.randint(1, 2))
    for med_nombre, indicaciones in meds_Elegidos:
        cursor.execute("""
            INSERT INTO detalle_recetas (receta_id, medicamento, indicaciones, cantidad) 
            VALUES (%s, %s, %s, %s)
        """, (receta_id, med_nombre, indicaciones, random.randint(1, 3)))

print("[+] Fase 5 Completada")
print("[*] Comenzando Fase 6: Laboratorio y Estudios")
print("\n[*] Recuperando consultas, pacientes y médicos...")

cursor.execute("SELECT id_consulta, paciente_id, medico_id FROM consultas")
consultas = cursor.fetchall()

# ---------------------------------------------------------
# 22. TIPOS DE ESTUDIOS (Catálogo)
# ---------------------------------------------------------
print("\n[*] Generando Catálogo de Tipos de Estudios...")

estudios_catalogo = [
    ("Resonancia Magnética Nuclear (RMN)", "Imagen de alta resolución de cerebro o columna."),
    ("Tomografía Computada (TAC)", "Estudio transversal de órganos internos."),
    ("Análisis de Sangre Completo", "Hemograma completo, ionograma y función renal."),
    ("Punción Lumbar", "Extracción de líquido cefalorraquídeo para descartar infecciones o esclerosis."),
    ("Ecografía Abdominal", "Evaluación de órganos en la cavidad abdominal."),
    ("Panel Toxicológico", "Búsqueda de metales pesados, drogas o venenos en sangre."),
    ("Biopsia de Tejido", "Análisis microscópico de muestras de tejido para descartar amiloidosis o cáncer.")
]

estudio_tipo_ids = []

for nombre, desc in estudios_catalogo:
    cursor.execute("""
        INSERT INTO tipos_estudios (nombre, descripcion) 
        VALUES (%s, %s)
    """, (nombre, desc))
    estudio_tipo_ids.append(cursor.lastrowid)
    print(f" - Estudio registrado: {nombre}")

# ---------------------------------------------------------
# 23. ÓRDENES DE ESTUDIOS Y RESULTADOS
# ---------------------------------------------------------
print("\n[*] Generando Órdenes de Estudios y sus Resultados...")

estados_estudio = ['Completado', 'Pendiente', 'En proceso']

for consulta in consultas[:12]: # Generamos órdenes para las primeras consultas
    tipo_estudio_id = random.choice(estudio_tipo_ids)
    estado = random.choice(estados_estudio)
    
    # Insertar la orden de estudio
    cursor.execute("""
        INSERT INTO ordenes_estudios (consulta_id, paciente_id, medico_id, tipo_estudio_id, fecha_orden, estado) 
        VALUES (%s, %s, %s, %s, NOW(), %s)
    """, (
        consulta['id_consulta'], 
        consulta['paciente_id'], 
        consulta['medico_id'], 
        tipo_estudio_id, 
        estado
    ))
    
    orden_id = cursor.lastrowid
    
    # Si el estudio está completado, generamos su resultado
    if estado == 'Completado':
        observaciones_resultado = fake.text(max_nb_chars=120)
        resultado_texto = "Valores dentro de parámetros normales. Descartado cuadro autoinmune agudo."
        
        # Pequeño guiño ocasional
        if random.random() < 0.2:
            resultado_texto = "Resultados inconclusos. El paciente miente sobre sus síntomas. Reevaluar."

        cursor.execute("""
            INSERT INTO resultados_estudios (orden_estudio_id, resultado, observaciones, fecha_resultado) 
            VALUES (%s, %s, %s, NOW())
        """, (orden_id, resultado_texto, observaciones_resultado))

print("[+] Fase 6 completada.")
print("[*] Comenzando Fase 7: Farmacia, Stock")
# ---------------------------------------------------------
# 24. PROVEEDORES
# ---------------------------------------------------------
print("\n[*] Registrando Proveedores Farmacéuticos...")

proveedores_data = [
    ("Droguería Princeton Pharma", "Av. Libertador 4500, CABA", "011-4555-1234"),
    ("Laboratorios Diagnostic Corp", "Panamericana Km 35, Buenos Aires", "011-4777-9876"),
    ("BioSuministros del Plata", "Corrientes 1200, CABA", "011-4333-5678"),
    ("Global Medical Supplies", "San Martín 800, Rosario", "0341-422-1111")
]

proveedor_ids = []

for nombre, direccion, telefono in proveedores_data:
    cursor.execute("""
        INSERT INTO proveedores (nombre, direccion, telefono) 
        VALUES (%s, %s, %s)
    """, (nombre, direccion, telefono))
    proveedor_ids.append(cursor.lastrowid)
    print(f" - Proveedor: {nombre}")

# ---------------------------------------------------------
# 25. MEDICAMENTO_INSUMOS (Inventario base)
# ---------------------------------------------------------
print("\n[*] Registrando Catálogo de Medicamentos e Insumos...")

medicamentos_insumos = [
    ("Vicodin 10mg", "Analgésico opioide de uso restringido (Control estricto de House)", "Comprimidos"),
    ("Ibuprofeno 600mg", "Antiinflamatorio no esteroideo", "Comprimidos"),
    ("Paracetamol 500mg", "Analgésico y antipirético", "Comprimidos"),
    ("Suero Fisiológico 0.9%", "Solución inyectable para hidratación y vía", "Bolsa 500ml"),
    ("Metotrexato 2.5mg", "Inmunosupresor para patologías autoinmunes", "Comprimidos"),
    ("Placebo de Sacarosa", "Comprimidos de azúcar puro para pacientes sin patología real", "Comprimidos"),
    ("Adrenalina 1mg/ml", "Vasopresor para emergencias en shock anafiláctico", "Ampollas")
]

insumo_ids = []

for nombre, desc, presentacion in medicamentos_insumos:
    cursor.execute("""
        INSERT INTO medicamento_insumos (nombre, descripcion, presentacion) 
        VALUES (%s, %s, %s)
    """, (nombre, desc, presentacion))
    insumo_ids.append(cursor.lastrowid)
    print(f" - Insumo registrado: {nombre}")

# ---------------------------------------------------------
# 26. LOTES_MEDICAMENTOS
# ---------------------------------------------------------
print("\n[*] Generando Lotes de Medicamentos y Stock...")

lote_ids = []

for insumo_id in insumo_ids:
    prov_id = random.choice(proveedor_ids)
    nro_lote = f"LOT-{random.randint(10000, 99999)}"
    stock_actual = random.randint(50, 500)
    fecha_vencimiento = fake.date_between(start_date='+6m', end_date='+2y')

    cursor.execute("""
        INSERT INTO lotes_medicamentos (medicamento_insumo_id, proveedor_id, numero_lote, stock_actual, fecha_vencimiento) 
        VALUES (%s, %s, %s, %s, %s)
    """, (insumo_id, prov_id, nro_lote, stock_actual, fecha_vencimiento))
    lote_ids.append(cursor.lastrowid)

print(" - Lotes de medicamentos cargados al depósito central.")

# ---------------------------------------------------------
# 27. MOVIMIENTO_STOCK
# ---------------------------------------------------------
print("\n[*] Registrando Movimientos de Stock (Entradas y Salidas)...")

for lote_id in lote_ids[:5]:
    tipo_mov = random.choice(['Entrada', 'Salida'])
    cantidad = random.randint(10, 50)
    motivo = "Reposición mensual de farmacia" if tipo_mov == 'Entrada' else "Despacho a piso de internación"

    cursor.execute("""
        INSERT INTO movimiento_stock (lote_medicamento_id, tipo_movimiento, cantidad, motivo, fecha) 
        VALUES (%s, %s, %s, %s, NOW())
    """, (lote_id, tipo_mov, cantidad, motivo))

# ---------------------------------------------------------
# 28. DISPENSACION_FARMACIA
# ---------------------------------------------------------
print("\n[*] Registrando Dispensaciones de Farmacia a Pacientes...")

cursor.execute("SELECT id_paciente FROM pacientes")
pacientes_dispensacion = [row['id_paciente'] for row in cursor.fetchall()]

for i in range(8):
    pac_id = random.choice(pacientes_dispensacion)
    lote_id = random.choice(lote_ids)
    cantidad_retirada = random.randint(1, 3)

    cursor.execute("""
        INSERT INTO dispensacion_farmacia (paciente_id, lote_medicamento_id, cantidad, fecha_dispensacion) 
        VALUES (%s, %s, %s, NOW())
    """, (pac_id, lote_id, cantidad_retirada))

print("[+] Fase 7 Completada")
print("[*] Comenzando Fase 8: Quirofanos")
print("\n[*] Recuperando pacientes, médicos y enfermeros...")

cursor.execute("SELECT id_paciente FROM pacientes")
pacientes = [row['id_paciente'] for row in cursor.fetchall()]

cursor.execute("""
    SELECT e.id_empleado 
    FROM empleados e 
    JOIN usuarios u ON e.usuario_id = u.id_usuario 
    WHERE u.rol = 'medico'
""")
medicos = [row['id_empleado'] for row in cursor.fetchall()]

cursor.execute("""
    SELECT e.id_empleado 
    FROM empleados e 
    JOIN usuarios u ON e.usuario_id = u.id_usuario 
    WHERE u.rol = 'enfermero'
""")
enfermeros = [row['id_empleado'] for row in cursor.fetchall()]

# ---------------------------------------------------------
# 29. QUIROFANOS
# ---------------------------------------------------------
print("\n[*] Registrando Quirófanos...")

quirofanos_data = [
    ("Quirófano Central #1", "Alta complejidad / Cardiovascular"),
    ("Quirófano Central #2", "Cirugía general y laparoscopia"),
    ("Quirófano de Urgencias #3", "Guardia / Traumatología de emergencia"),
    ("Quirófano Neurológico #4", "Neurocirugía avanzada")
]

quirofano_ids = []

for nombre, desc in quirofanos_data:
    cursor.execute("""
        INSERT INTO quirofanos (nombre, descripcion, estado) 
        VALUES (%s, %s, 'Disponible')
    """, (nombre, desc))
    quirofano_ids.append(cursor.lastrowid)
    print(f" - Quirófano: {nombre}")

# ---------------------------------------------------------
# 30. CIRUGIAS PROGRAMADAS
# ---------------------------------------------------------
print("\n[*] Programando Intervenciones Quirúrgicas...")

tipos_cirugias = [
    ("Biopsia cerebral profunda", "Extracción de tejido para diagnóstico diferencial."),
    ("Reparación de aneurisma abdominal", "Urgencia vascular."),
    ("Laparoscopia exploratoria", "Búsqueda de causa de dolor abdominal idiopático."),
    ("Osteosíntesis de fémur", "Reducción de fractura por traumatismo de guardia.")
]

cirugia_ids = []

for i in range(5):
    paciente_id = random.choice(pacientes)
    quirofano_id = random.choice(quirofano_ids)
    cirugia_nombre, descripcion = random.choice(tipos_cirugias)
    
    fecha_cirugia = fake.date_time_between(start_date='-10d', end_date='+15d')
    estado = random.choice(['Programada', 'Completada', 'En curso', 'Cancelada'])

    cursor.execute("""
        INSERT INTO cirugias_programadas (paciente_id, quirofano_id, tipo_cirugia, descripcion, fecha_programada, estado) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (paciente_id, quirofano_id, cirugia_nombre, descripcion, fecha_cirugia, estado))
    
    cirugia_ids.append(cursor.lastrowid)
    print(f" - Cirugía agendada: {cirugia_nombre} (Quirófano ID: {quirofano_id})")

# =========================================================
# #Author: Amanda Julieta
# #Version: 1.1
# #Date: 2026-08-14 America/South_America/Argentina
# =========================================================

import mysql.connector
from faker import Faker
import random
from datetime import datetime, timedelta

print("==== Fase 9: Facturación, Auditoría y Cierre ====")
print("==== JustAnother Hospital === - Configuración Final...")
fake = Faker('es_AR')

# Establecer conexión
try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password=''
    )
    cursor = conn.cursor(dictionary=True)
    print("[*] Conexión establecida exitosamente para la Fase Final...")
except mysql.connector.Error as err:
    print(f"[!] Error al conectar a la base de datos: {err}")
    exit(1)

# Seleccionar la base de datos
cursor.execute("USE db_justanother_hospital")

# ---------------------------------------------------------
# 31. RECUPERAR DATOS NECESARIOS
# ---------------------------------------------------------
print("\n[*] Recuperando pacientes y cirugías para facturación y auditoría...")

cursor.execute("SELECT id_paciente FROM pacientes")
pacientes = [row['id_paciente'] for row in cursor.fetchall()]

cursor.execute("SELECT id_cirugia, paciente_id FROM cirugias_programadas")
cirugias = cursor.fetchall()

cursor.execute("""
    SELECT e.id_empleado, u.rol 
    FROM empleados e 
    JOIN usuarios u ON e.usuario_id = u.id_usuario 
    WHERE u.rol = 'administrativo'
""")
administrativos = [row['id_empleado'] for row in cursor.fetchall()]

# ---------------------------------------------------------
# 32. FACTURACIÓN Y PAGOS
# ---------------------------------------------------------
print("\n[*] Generando registros de Facturación...")

estados_pago = ['Pagado', 'Pendiente', 'Rechazado por Cobertura', 'En litigio (House rompió algo)']

for i in range(15):
    paciente_id = random.choice(pacientes)
    monto = round(random.uniform(15000.00, 450000.00), 2)
    estado = random.choice(estados_pago)
    
    cursor.execute("""
        INSERT INTO facturacion (paciente_id, monto_total, estado_pago, fecha_emision) 
        VALUES (%s, %s, %s, NOW())
    """, (paciente_id, monto, estado))

print(" - Facturas emitidas correctamente.")

# ---------------------------------------------------------
# 33. AUDITORÍA / REGISTRO DE ACTIVIDAD DEL SISTEMA
# ---------------------------------------------------------
print("\n[*] Generando registros de Auditoría del Sistema...")

acciones_auditoria = [
    "Inicio de sesión de usuario",
    "Modificación de historia clínica",
    "Acceso restringido a inventario",
    "Intento fallido de acceso por credenciales incorrectas",
    "Egreso de paciente de terapia intensiva"
]

if administrativos: 
    for _ in range(20):
        admin_id = random.choice(administrativos)
        accion = random.choice(acciones_auditoria)
        detalles = fake.sentence(nb_words=8)
        
        cursor.execute("""
            INSERT INTO auditoria_sistema (empleado_id, accion, detalles, fecha_hora) 
            VALUES (%s, %s, %s, NOW())
        """, (admin_id, accion, detalles))

print(" - Auditoría del sistema registrada con éxito.")

# ---------------------------------------------------------
# 35. EQUIPO QUIRURGICO (Tabla puente)
# ---------------------------------------------------------
print("\n[*] Asignando Equipos Quirúrgicos a las cirugías...")

for cirugia_id in cirugia_ids:
    # Asignamos 1 o 2 médicos principales/ayudantes
    if medicos:
        medicos_asignados = random.sample(medicos, min(len(medicos), random.randint(1, 2)))
        for med_id in medicos_asignados:
            cursor.execute("""
                INSERT INTO equipo_quirugico (cirugia_id, empleado_id, rol_quirurgico) 
                VALUES (%s, %s, 'Cirujano Principal')
            """, (cirugia_id, med_id))

    # Asignamos 1 enfermero instrumentista si hay disponibles
    if enfermeros:
        enf_id = random.choice(enfermeros)
        cursor.execute("""
            INSERT INTO equipo_quirugico (cirugia_id, empleado_id, rol_quirurgico) 
            VALUES (%s, %s, 'Enfermero Instrumentista')
        """, (cirugia_id, enf_id))

print("[+] Fase 7 Completada")
print("[*] Comenzando Fase 9: Facturación")

# ---------------------------------------------------------
# 36. RECUPERAR PACIENTES Y COBERTURAS
# ---------------------------------------------------------
print("\n[*] Recuperando pacientes y coberturas...")

cursor.execute("SELECT id_paciente FROM pacientes")
pacientes = [row['id_paciente'] for row in cursor.fetchall()]

cursor.execute("SELECT id_cobertura, paciente_id, obra_social_id FROM pacientes_cobertura")
coberturas = cursor.fetchall()
cobertura_dict = {c['paciente_id']: c['id_cobertura'] for c in coberturas}

# ---------------------------------------------------------
# 3. TARIFARIO (Catálogo de precios)
# ---------------------------------------------------------
print("\n[*] Registrando Tarifario de Servicios Médicos...")

tarifas_data = [
    ("Consulta Médica General / Guardia", "Consulta", 15000.00),
    ("Consulta Especializada (Diagnóstico)", "Consulta", 35000.00),
    ("Resonancia Magnética (RMN)", "Estudio", 85000.00),
    ("Análisis de Sangre Completo", "Estudio", 12000.00),
    ("Cirugía Mayor / Exploratoria", "Cirugía", 250000.00),
    ("Día de Internación en UTI", "Internación", 120000.00)
]

tarifario_ids = []

for concepto, tipo, precio in tarifas_data:
    cursor.execute("""
        INSERT INTO tarifario (concepto, tipo_servicio, precio) 
        VALUES (%s, %s, %s)
    """, (concepto, tipo, precio))
    tarifario_ids.append(cursor.lastrowid)
    print(f" - Servicio: {concepto} | Precio: ${precio}")

# ---------------------------------------------------------
# 37. FACTURAS
# ---------------------------------------------------------
print("\n[*] Generando Facturas Médicas...")

factura_ids = []
estados_factura = ['Pagada', 'Pendiente', 'Rechazada por Prepaga']

for i in range(10):
    paciente_id = random.choice(pacientes)
    cobertura_id = cobertura_dict.get(paciente_id, None)
    total = round(random.uniform(15000.00, 300000.00), 2)
    estado = random.choice(estados_factura)

    cursor.execute("""
        INSERT INTO facturas (paciente_id, paciente_cobertura_id, fecha_emision, monto_total, estado) 
        VALUES (%s, %s, NOW(), %s, %s)
    """, (paciente_id, cobertura_id, total, estado))
    
    factura_ids.append(cursor.lastrowid)

print(f" - Generadas {len(factura_ids)} facturas en el sistema.")

# ---------------------------------------------------------
# 38. DETALLE_FACTURA
# ---------------------------------------------------------
print("\n[*] Agregando Detalles a las Facturas...")

for factura_id in factura_ids[:8]:
    # Asignamos 1 o 2 ítems del tarifario a cada factura
    cantidad_items = random.randint(1, 2)
    for _ in range(cantidad_items):
        tarifa_id = random.choice(tarifario_ids)
        cantidad = random.randint(1, 2)
        subtotal = round(cantidad * random.uniform(15000.00, 85000.00), 2)

        cursor.execute("""
            INSERT INTO detalle_factura (factura_id, tarifario_id, cantidad, subtotal) 
            VALUES (%s, %s, %s, %s)
        """, (factura_id, tarifa_id, cantidad, subtotal))

print(" - Detalles de factura registrados.")

# ---------------------------------------------------------
# 39. PAGOS
# ---------------------------------------------------------
print("\n[*] Registrando Pagos...")

metodos_pago = ['Tarjeta de Crédito', 'Transferencia Bancaria', 'Obra Social / Prepaga', 'Efectivo']

for factura_id in factura_ids[:6]: # Registramos pagos para las primeras facturas
    monto_pagado = round(random.uniform(20000.00, 250000.00), 2)
    metodo = random.choice(metodos_pago)

    cursor.execute("""
        INSERT INTO pagos (factura_id, monto, metodo_pago, fecha_pago) 
        VALUES (%s, %s, %s, NOW())
    """, (factura_id, monto_pagado, metodo))

print("[+] Fase 9 completada.")

# Guardar cambios y cerrar conexión
conn.commit()
cursor.close()
conn.close()
print("[+] Proceso finalizado exitosamente.")