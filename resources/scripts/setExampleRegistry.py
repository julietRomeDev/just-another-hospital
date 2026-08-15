#Author: Amanda Julieta
#Version: 1.1
#Date: 2026-08-14 America/South_America/Argentina


import mysql.connector
from faker import Faker
print("====Just Another Hospital - Fake Users Config...")
fake = Faker('es_AR')

#Establecer conexión
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password=''
)
cursor = conn.cursor()
print("[*] Conexion establecida exitosamente...")

#Validación de conexión
try:
    cursor.execute("SELECT VERSION();")
    version = cursor.fetchone()
    print(f"[*] Base de datos conectada correctamente: Current Version: {version[0]}")
except:
    print(f"[!] Error al validar la conexion: {e}")
    
#Seleccionar la base de datos
cursor.execute("USE db_justanother_hospital")
print("[*] Generando usuarios... ")
print("")

roles = ['medico', 'enfermero', 'farmaceutico', 'administrativo']

for rol in roles:
    print(f"[*] Generando cinco {rol}es")

    for _ in range(5):
        nombre = fake.first_name()
        apellido = fake.last_name()
        nombre_usuario = fake.user_name()
        password = fake.password(length=10)
        email = fake.ascii_free_email()

        
        cursor.execute(
            "INSERT INTO usuarios (nombre, apellido, nombre_usuario, email, password rol) VALUES (%s, %s, %s, %s, %s)",
            (nombre, apellido, nombre_usuario, email, password, rol)
        )
        
        print()
        print(f" - Nombre: {nombre} | Apellido: {apellido}")
        print(f"    - Usuario: {nombre_usuario} | Rol: {rol} | Email: {email} | Password: {password}")


conn.commit()
cursor.close()
conn.close()
print("[+] Proceso finalizado.")