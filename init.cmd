@echo off
title Configure Environment - Just Another Hospital
color 0b

echo ========================================================
echo       CONFIGURACION DEL ENTORNO - HOSPITAL DB
echo ========================================================
echo.
echo [!] Asegurate de que Laragon o XAMPP tengan MySQL activo.
echo [!] Asegurate de tener Python instalado.
echo.
pause

echo [*] Instalando Dependendencias [Python]:
pip install faker 
pip install mysql-connector

:: Verificacion del Archivo .bat/cmd
cd /d "%~dp0"

:: Verificamos que la carpeta de recursos exista
if not exist "resources\scripts" (
    color 0c
    echo.
    echo [X] ERROR: No se encuentra la carpeta "resources\scripts".
    echo [X] Asegurate de que la estructura sea la correcta.
    pause
    exit /b
)

:: Entramos a la carpeta de scripts
cd resources\scripts

color 0a
cls
echo [*] Ejecutando script de creacion de base de datos...
python createDatabase.py

if %errorlevel% neq 0 (
    color 0c
    echo.
    echo [X] ERROR: Fallo al crear la base de datos. 
    echo [X] Revisa que MySQL este encendido en tu servidor.
    pause
    exit /b %errorlevel%
)
echo [+] Base de datos creada con exito.

echo.
cls
echo [*] Registrando datos de ejemplo...
python setExampleRegistry.py

if %errorlevel% neq 0 (
    color 0c
    echo.
    echo [X] ERROR: Fallo al insertar los registros de ejemplo.
    pause
    exit /b %errorlevel%
)
echo [+] Datos de ejemplo cargados correctamente.

color 0a
echo.
echo ========================================================
echo [+] Entorno configurado y listo para usar.
echo ========================================================
echo.
pause
color 07