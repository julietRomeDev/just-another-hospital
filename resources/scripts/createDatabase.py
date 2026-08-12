# Author: Amanda Julieta
# Version: 1.1
# Date: 2026-08-11 America/South_America/Argentina

import mysql.connector

# Establecer la conexión con MySQL
conn = mysql.connector.connect(
    host="localhost", 
    user="root", 
    password=""
)
cursor = conn.cursor()

# Crear y seleccionar la base de datos
cursor.execute("CREATE DATABASE IF NOT EXISTS db_justanother_hospital")
print("[*] Base de Datos creada exitosamente!")

cursor.execute("USE db_justanother_hospital")
print("[*] Usando la base de datos db_justanother_hospital")

print("[*] Eliminando tablas...")
cursor.execute("DROP TABLE IF EXISTS pagos")
cursor.execute("DROP TABLE IF EXISTS detalle_factura")
cursor.execute("DROP TABLE IF EXISTS facturas")
cursor.execute("DROP TABLE IF EXISTS tarifario")
cursor.execute("DROP TABLE IF EXISTS equipo_quirugico")
cursor.execute("DROP TABLE IF EXISTS cirugias_programadas")
cursor.execute("DROP TABLE IF EXISTS quirofanos")
cursor.execute("DROP TABLE IF EXISTS dispensacion_farmacia")
cursor.execute("DROP TABLE IF EXISTS movimiento_stock")
cursor.execute("DROP TABLE IF EXISTS proveedores")
cursor.execute("DROP TABLE IF EXISTS lotes_medicamentos")
cursor.execute("DROP TABLE IF EXISTS medicamento_insumos")
cursor.execute("DROP TABLE IF EXISTS resultados_estudios")
cursor.execute("DROP TABLE IF EXISTS ordenes_estudios")
cursor.execute("DROP TABLE IF EXISTS tipos_estudios")
cursor.execute("DROP TABLE IF EXISTS box_guardia")
cursor.execute("DROP TABLE IF EXISTS triage")
cursor.execute("DROP TABLE IF EXISTS evoluciones_internacion")
cursor.execute("DROP TABLE IF EXISTS detalle_recetas")
cursor.execute("DROP TABLE IF EXISTS recetas_medicas")
cursor.execute("DROP TABLE IF EXISTS signos_vitales")
cursor.execute("DROP TABLE IF EXISTS consulta_diagnostico")
cursor.execute("DROP TABLE IF EXISTS diagnosticos")
cursor.execute("DROP TABLE IF EXISTS consultas")
cursor.execute("DROP TABLE IF EXISTS turnos")
cursor.execute("DROP TABLE IF EXISTS agenda_medica")
cursor.execute("DROP TABLE IF EXISTS enfermeros_sectores")
cursor.execute("DROP TABLE IF EXISTS camas")
cursor.execute("DROP TABLE IF EXISTS habitaciones")
cursor.execute("DROP TABLE IF EXISTS sectores")
cursor.execute("DROP TABLE IF EXISTS pisos_edificio")
cursor.execute("DROP TABLE IF EXISTS horario_personal")
cursor.execute("DROP TABLE IF EXISTS enfermeras_turnos")
cursor.execute("DROP TABLE IF EXISTS medicos_especialidades")
cursor.execute("DROP TABLE IF EXISTS especialidades")
cursor.execute("DROP TABLE IF EXISTS empleados")
cursor.execute("DROP TABLE IF EXISTS pacientes_cobertura")
cursor.execute("DROP TABLE IF EXISTS obras_sociales_prepagas")
cursor.execute("DROP TABLE IF EXISTS contactos_emergencia")
cursor.execute("DROP TABLE IF EXISTS pacientes")
print("[*] Tablas eliminadas exitosamente...")

print("[*] Creando tablas...")
print("[**] Creando tablas Pacientes e Identidad")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Obras_Sociales_Prepagas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        cuit VARCHAR(20) NOT NULL,
        plan VARCHAR(50),
        tipo_cobertura VARCHAR(50)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Pacientes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        dni VARCHAR(20) NOT NULL UNIQUE,
        nombre VARCHAR(50) NOT NULL,
        apellido VARCHAR(50) NOT NULL,
        fecha_nacimiento DATE NOT NULL,
        genero VARCHAR(20),
        grupo_sanguineo VARCHAR(10),
        direccion VARCHAR(150),
        telefono VARCHAR(30),
        email VARCHAR(100)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Contactos_Emergencia (
        id INT AUTO_INCREMENT PRIMARY KEY,
        paciente_id INT NOT NULL,
        nombre VARCHAR(100) NOT NULL,
        parentesco VARCHAR(50),
        telefono VARCHAR(30) NOT NULL,
        direccion VARCHAR(150),
        FOREIGN KEY (paciente_id) REFERENCES Pacientes(id) ON DELETE CASCADE
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Pacientes_Coberturas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        paciente_id INT NOT NULL,
        cobertura_id INT NOT NULL,
        numero_afiliado VARCHAR(50) NOT NULL,
        fecha_vigencia DATE,
        FOREIGN KEY (paciente_id) REFERENCES Pacientes(id) ON DELETE CASCADE,
        FOREIGN KEY (cobertura_id) REFERENCES Obras_Sociales_Prepagas(id)
    )
""")

print("[*] TABLA CREADA CON EXITO")
print("[+] CREANDO TABLAS PERSONAL MEDICO Y ADMINISTRATIVO")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Empleados (
        id INT AUTO_INCREMENT PRIMARY KEY,
        legajo VARCHAR(20) NOT NULL UNIQUE,
        dni VARCHAR(20) NOT NULL UNIQUE,
        nombre VARCHAR(50) NOT NULL,
        apellido VARCHAR(50) NOT NULL,
        fecha_ingreso DATE NOT NULL,
        tipo_empleado ENUM('medico', 'enfermero', 'administrativo', 'tecnico') NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Especialidades (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre_especialidad VARCHAR(100) NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Medicos_Especialidades (
        id INT AUTO_INCREMENT PRIMARY KEY,
        empleado_id INT NOT NULL,
        especialidad_id INT NOT NULL,
        numero_matricula VARCHAR(50) NOT NULL UNIQUE,
        FOREIGN KEY (empleado_id) REFERENCES Empleados(id) ON DELETE CASCADE,
        FOREIGN KEY (especialidad_id) REFERENCES Especialidades(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Horarios_Personal (
        id INT AUTO_INCREMENT PRIMARY KEY,
        empleado_id INT NOT NULL,
        dia_semana VARCHAR(20) NOT NULL,
        hora_inicio TIME NOT NULL,
        hora_fin TIME NOT NULL,
        FOREIGN KEY (empleado_id) REFERENCES Empleados(id) ON DELETE CASCADE
    )
""")

print("[+] TABLA PERSONAL CREADA CON EXITO")
print("[*] CREANDO TABLAS INFRAESTRUCTURA MEDICA")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Pisos_Edificio (
        id INT AUTO_INCREMENT PRIMARY KEY,
        numero_piso INT NOT NULL,
        descripcion VARCHAR(100)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Sectores (
        id INT AUTO_INCREMENT PRIMARY KEY,
        piso_id INT NOT NULL,
        nombre_sector VARCHAR(100) NOT NULL,
        FOREIGN KEY (piso_id) REFERENCES Pisos_Edificio(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Habitaciones (
        id INT AUTO_INCREMENT PRIMARY KEY,
        sector_id INT NOT NULL,
        numero_habitacion VARCHAR(20) NOT NULL,
        tipo ENUM('individual', 'compartida', 'aislamiento', 'uti') NOT NULL,
        FOREIGN KEY (sector_id) REFERENCES Sectores(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Camas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        habitacion_id INT NOT NULL,
        codigo_cama VARCHAR(20) NOT NULL,
        estado ENUM('libre', 'ocupada', 'mantenimiento') DEFAULT 'libre',
        FOREIGN KEY (habitacion_id) REFERENCES Habitaciones(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Enfermeros_Sectores (
        id INT AUTO_INCREMENT PRIMARY KEY,
        empleado_id INT NOT NULL,
        sector_id INT NOT NULL,
        FOREIGN KEY (empleado_id) REFERENCES Empleados(id),
        FOREIGN KEY (sector_id) REFERENCES Sectores(id)
    )
""")

print("[+] TABLA CREADA EXITOSAMENTE")
print("[*] CREANDO TABLAS ADMISION")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Agenda_Medica (
        id INT AUTO_INCREMENT PRIMARY KEY,
        empleado_id INT NOT NULL,
        fecha_hora_inicio DATETIME NOT NULL,
        fecha_hora_fin DATETIME NOT NULL,
        cupo_maximo INT NOT NULL,
        FOREIGN KEY (empleado_id) REFERENCES Empleados(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Turnos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        agenda_id INT NOT NULL,
        paciente_id INT NOT NULL,
        fecha_hora_turno DATETIME NOT NULL,
        estado ENUM('pendiente', 'confirmado', 'cancelado', 'atendido') DEFAULT 'pendiente',
        FOREIGN KEY (agenda_id) REFERENCES Agenda_Medica(id),
        FOREIGN KEY (paciente_id) REFERENCES Pacientes(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Consultas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        turno_id INT UNIQUE,
        paciente_id INT NOT NULL,
        empleado_id INT NOT NULL,
        motivo_consulta TEXT NOT NULL,
        observaciones TEXT,
        fecha_hora_atencion DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (turno_id) REFERENCES Turnos(id),
        FOREIGN KEY (paciente_id) REFERENCES Pacientes(id),
        FOREIGN KEY (empleado_id) REFERENCES Empleados(id)
    )
""")

print("[+] TABLA CREADA EXITOSAMENTE")
print("[*] CREANDO TABLAS CLINICO")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Diagnosticos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        codigo_cie10 VARCHAR(20) NOT NULL UNIQUE,
        descripcion_enfermedad VARCHAR(255) NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Consulta_Diagnosticos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        consulta_id INT NOT NULL,
        diagnostico_id INT NOT NULL,
        tipo ENUM('presuntivo', 'definitivo') DEFAULT 'definitivo',
        FOREIGN KEY (consulta_id) REFERENCES Consultas(id) ON DELETE CASCADE,
        FOREIGN KEY (diagnostico_id) REFERENCES Diagnosticos(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Signos_Vitales (
        id INT AUTO_INCREMENT PRIMARY KEY,
        consulta_id INT,
        paciente_id INT NOT NULL,
        presion_arterial VARCHAR(20),
        frecuencia_cardiaca INT,
        temperatura DECIMAL(4,2),
        saturacion_oxigeno INT,
        peso DECIMAL(5,2),
        altura DECIMAL(3,2),
        fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (consulta_id) REFERENCES Consultas(id),
        FOREIGN KEY (paciente_id) REFERENCES Pacientes(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Recetas_Medicas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        consulta_id INT NOT NULL,
        paciente_id INT NOT NULL,
        empleado_id INT NOT NULL,
        fecha_emision DATETIME DEFAULT CURRENT_TIMESTAMP,
        indicaciones_generales TEXT,
        FOREIGN KEY (consulta_id) REFERENCES Consultas(id),
        FOREIGN KEY (paciente_id) REFERENCES Pacientes(id),
        FOREIGN KEY (empleado_id) REFERENCES Empleados(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Evoluciones_Internacion (
        id INT AUTO_INCREMENT PRIMARY KEY,
        paciente_id INT NOT NULL,
        cama_id INT NOT NULL,
        empleado_id INT NOT NULL,
        nota_evolucion TEXT NOT NULL,
        fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (paciente_id) REFERENCES Pacientes(id),
        FOREIGN KEY (cama_id) REFERENCES Camas(id),
        FOREIGN KEY (empleado_id) REFERENCES Empleados(id)
    )
""")

print("[+] TABLA CREADA EXITOSAMENTE")
print("[*] CREANDO TABLAS TRIAGE")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Triage (
        id INT AUTO_INCREMENT PRIMARY KEY,
        paciente_id INT NOT NULL,
        empleado_id INT NOT NULL,
        nivel_urgencia INT CHECK (nivel_urgencia BETWEEN 1 AND 5),
        sintomas_principales TEXT NOT NULL,
        fecha_hora_ingreso DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (paciente_id) REFERENCES Pacientes(id),
        FOREIGN KEY (empleado_id) REFERENCES Empleados(id)
    )
""")

print("[+] TABLA CREADA EXITOSAMENTE")
print("[*] CREANDO TABLAS ESTUDIOS")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Tipos_Estudios (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre_estudio VARCHAR(150) NOT NULL,
        categoria VARCHAR(100)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Ordenes_Estudios (
        id INT AUTO_INCREMENT PRIMARY KEY,
        consulta_id INT NOT NULL,
        paciente_id INT NOT NULL,
        empleado_id INT NOT NULL,
        fecha_solicitud DATETIME DEFAULT CURRENT_TIMESTAMP,
        estado ENUM('pendiente', 'realizado', 'cancelado') DEFAULT 'pendiente',
        FOREIGN KEY (consulta_id) REFERENCES Consultas(id),
        FOREIGN KEY (paciente_id) REFERENCES Pacientes(id),
        FOREIGN KEY (empleado_id) REFERENCES Empleados(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Resultados_Estudios (
        id INT AUTO_INCREMENT PRIMARY KEY,
        orden_estudio_id INT NOT NULL UNIQUE,
        tecnico_id INT NOT NULL,
        resultado_texto TEXT NOT NULL,
        archivo_adjunto_path VARCHAR(255),
        fecha_realizacion DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (orden_estudio_id) REFERENCES Ordenes_Estudios(id),
        FOREIGN KEY (tecnico_id) REFERENCES Empleados(id)
    )
""")

print("[+] TABLA CREADA EXITOSAMENTE")
print("[*] CREANDO TABLAS INVENTARIO")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Medicamentos_Insumos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        codigo_barra VARCHAR(50) UNIQUE,
        nombre_comercial VARCHAR(100) NOT NULL,
        monodroga VARCHAR(100),
        presentacion VARCHAR(50),
        stock_minimo INT NOT NULL,
        stock_actual INT NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Proveedores (
        id INT AUTO_INCREMENT PRIMARY KEY,
        razon_social VARCHAR(150) NOT NULL,
        cuit VARCHAR(20) NOT NULL,
        telefono VARCHAR(30),
        email VARCHAR(100),
        direccion VARCHAR(150)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Lotes_Medicamentos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        medicamento_id INT NOT NULL,
        proveedor_id INT,
        numero_lote VARCHAR(50) NOT NULL,
        fecha_vencimiento DATE NOT NULL,
        cantidad INT NOT NULL,
        FOREIGN KEY (medicamento_id) REFERENCES Medicamentos_Insumos(id),
        FOREIGN KEY (proveedor_id) REFERENCES Proveedores(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Movimientos_Stock (
        id INT AUTO_INCREMENT PRIMARY KEY,
        medicamento_id INT NOT NULL,
        empleado_id INT NOT NULL,
        tipo_movimiento ENUM('ingreso_compra', 'salida_dispensacion', 'merma', 'ajuste') NOT NULL,
        cantidad INT NOT NULL,
        fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (medicamento_id) REFERENCES Medicamentos_Insumos(id),
        FOREIGN KEY (empleado_id) REFERENCES Empleados(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Detalle_Recetas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        receta_id INT NOT NULL,
        medicamento_id INT NOT NULL,
        dosis VARCHAR(100) NOT NULL,
        frecuencia VARCHAR(100) NOT NULL,
        duracion_tratamiento VARCHAR(50) NOT NULL,
        FOREIGN KEY (receta_id) REFERENCES Recetas_Medicas(id),
        FOREIGN KEY (medicamento_id) REFERENCES Medicamentos_Insumos(id)
    )
""")

print("[+] TABLA CREADA EXITOSAMENTE")
print("[*] CREANDO TABLAS QUIROFANO")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Quirofanos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        numero_quirofano VARCHAR(20) NOT NULL,
        estado ENUM('disponible', 'ocupado', 'limpieza', 'mantenimiento') DEFAULT 'disponible'
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Cirugias_Programadas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        quirofano_id INT NOT NULL,
        paciente_id INT NOT NULL,
        fecha_hora_inicio DATETIME NOT NULL,
        fecha_hora_fin DATETIME NOT NULL,
        tipo_cirugia VARCHAR(150) NOT NULL,
        estado ENUM('programada', 'en_curso', 'finalizada', 'suspendida') DEFAULT 'programada',
        FOREIGN KEY (quirofano_id) REFERENCES Quirofanos(id),
        FOREIGN KEY (paciente_id) REFERENCES Pacientes(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Equipo_Quirurgico (
        id INT AUTO_INCREMENT PRIMARY KEY,
        cirugia_id INT NOT NULL,
        empleado_id INT NOT NULL,
        rol_quirofano ENUM('cirujano_principal', 'primer_ayudante', 'instrumentista', 'anestesista') NOT NULL,
        FOREIGN KEY (cirugia_id) REFERENCES Cirugias_Programadas(id),
        FOREIGN KEY (empleado_id) REFERENCES Empleados(id)
    )
""")

print("[+] TABLA CREADA EXITOSAMENTE")
print("[*] CREANDO TABLAS FACTURACION")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Tarifario (
        id INT AUTO_INCREMENT PRIMARY KEY,
        codigo_practica VARCHAR(50) NOT NULL UNIQUE,
        descripcion VARCHAR(200) NOT NULL,
        valor_base DECIMAL(10,2) NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Facturas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        paciente_id INT NOT NULL,
        cobertura_id INT,
        fecha_emision DATETIME DEFAULT CURRENT_TIMESTAMP,
        monto_total DECIMAL(10,2) NOT NULL,
        estado ENUM('pendiente', 'pagada', 'anulada') DEFAULT 'pendiente',
        FOREIGN KEY (paciente_id) REFERENCES Pacientes(id),
        FOREIGN KEY (cobertura_id) REFERENCES Obras_Sociales_Prepagas(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Detalle_Factura (
        id INT AUTO_INCREMENT PRIMARY KEY,
        factura_id INT NOT NULL,
        descripcion_item VARCHAR(200) NOT NULL,
        cantidad INT NOT NULL,
        precio_unitario DECIMAL(10,2) NOT NULL,
        subtotal DECIMAL(10,2) NOT NULL,
        FOREIGN KEY (factura_id) REFERENCES Facturas(id) ON DELETE CASCADE
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Pagos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        factura_id INT NOT NULL,
        forma_pago ENUM('efectivo', 'transferencia', 'tarjeta_credito', 'tarjeta_debito', 'obra_social') NOT NULL,
        monto_pagado DECIMAL(10,2) NOT NULL,
        fecha_pago DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (factura_id) REFERENCES Facturas(id)
    )
""")

conn.commit()
cursor.close()
conn.close()
print("[+] BASE DE DATOS CREADA Y CONFIGURADA EXITOSAMENTE")